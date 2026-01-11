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