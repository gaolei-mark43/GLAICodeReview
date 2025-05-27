from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import ReviewRequest
from app.core.review_service import ReviewService
from app.utils.jwt_token import get_current_user

router = APIRouter()
review_service = ReviewService()

@router.post("/review")
async def create_review(
    request: ReviewRequest,
    current_user: str = Depends(get_current_user)
):
    """
    创建代码评审
    
    Args:
        request: 评审请求对象
        current_user: 当前登录用户
        
    Returns:
        评审报告
    """
    try:
        # 生成评审报告
        review_report = await review_service.generate_review_report(request)
        
        return {
            "status": "success",
            "data": review_report
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"评审生成失败: {str(e)}")

