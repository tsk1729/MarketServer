from typing import Optional, Dict, Any

from starlette.responses import JSONResponse

from logger import logger
from mongo import repo_manager


def save_creator(data,user_id):
    data =data.dict()
    try:
        update =  repo_manager.influencers.upsert({"_id":user_id}, data)
        logger.info(f"Updated lines: Modified: {update.modified_count},Matched:{update.matched_count}")
    except Exception as e:
        logger.error(e)
    return JSONResponse(status_code=200,content={'msg':'saved creator data'})


def get_creator(user_id):
    return repo_manager.influencers.read({"_id":user_id})


def submit_proof(influencer_id, post_id, proofs):
    proofs = proofs.model_dump(mode="json")
    proofs["influencer_id"] = influencer_id
    n = repo_manager.brand_post_submissions.upsert({"_id":post_id}, proofs)
    return JSONResponse(status_code=200, content ={'modified_count':n.modified_count,'matched_count':n.matched_count,'message':"Updated proof successfully"})

def get_posts(page_size,last_value,direction,sort_field):
    response = repo_manager.brand_posts.paginate(page_size=page_size,last_value=last_value,direction=direction,sort_field=sort_field)
    return response




def paginate_by_reward(
    query: Optional[Dict[str, Any]] = None,
    page_size: int = 10,
    direction: int = -1,  # -1 = highest reward first
    last_cursor: Optional[Dict[str, Any]] = None,
):
    """
    Cursor-based pagination sorted by reward inside keyValuePairs.

    Cursor format:
    {
        "reward": int,
        "_id": str
    }
    """
    query = query or {}

    pipeline = []

    # Base filter
    pipeline.append({"$match": query})

    # Extract reward (max reward if multiple entries exist)
    pipeline.append({
        "$addFields": {
            "reward_sort": {
                "$max": "$keyValuePairs.reward"
            }
        }
    })

    # Cursor filter (CRITICAL FIX)
    if last_cursor:
        reward = last_cursor["reward"]
        last_id = ObjectId(last_cursor["_id"])

        if direction == -1:
            pipeline.append({
                "$match": {
                    "$or": [
                        {"reward_sort": {"$lt": reward}},
                        {
                            "reward_sort": reward,
                            "_id": {"$gt": last_id}
                        }
                    ]
                }
            })
        else:
            pipeline.append({
                "$match": {
                    "$or": [
                        {"reward_sort": {"$gt": reward}},
                        {
                            "reward_sort": reward,
                            "_id": {"$gt": last_id}
                        }
                    ]
                }
            })

    # Stable sort
    pipeline.append({
        "$sort": {
            "reward_sort": direction,
            "_id": 1
        }
    })

    # Fetch one extra to detect next page
    pipeline.append({"$limit": page_size + 1})

    documents = list(repo_manager.brand_posts.collection.aggregate(pipeline))

    has_next = len(documents) > page_size
    documents = documents[:page_size]

    next_cursor = None
    if has_next:
        last = documents[-1]
        next_cursor = {
            "reward": last["reward_sort"],
            "_id": str(last["_id"])
        }

    # Cleanup output
    for doc in documents:
        doc["_id"] = str(doc["_id"])
        doc.pop("reward_sort", None)

    return {
        "data": documents,
        "next_cursor": next_cursor
    }


def subscribe_to_brand(influencer_id, post_id):
    n = repo_manager.brand_post_submissions.upsert({"_id":post_id}, {"influencer_id": influencer_id})
    logger.info(f"Matched count: {n.matched_count}, Modified count: {n.modified_count}")
    return JSONResponse(status_code=200, content={'modified_count': n.modified_count, 'matched_count': n.matched_count,
                                                  'message': "Updated proof successfully"})


def is_influencer_subscribed(influencer_id, post_id):
    doc = repo_manager.brand_post_submissions.read({"_id":post_id, "influencer_id":influencer_id})
    if doc:
        return True
    else:
        return False
