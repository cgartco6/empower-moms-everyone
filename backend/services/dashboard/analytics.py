from sqlalchemy import func
from backend.models.payment import Transaction
from backend.models.course import Course

class RevenueTracker:
    @staticmethod
    def daily_revenue(days=30):
        return db.query(
            func.date(Transaction.created_at).label('date'),
            func.sum(Transaction.amount).label('revenue'),
            func.count(Transaction.id).label('transactions')
        ).filter(Transaction.status == 'completed') \
         .group_by(func.date(Transaction.created_at)) \
         .order_by(func.date(Transaction.created_at).desc()) \
         .limit(days).all()
    
    @staticmethod
    def top_selling_courses(limit=10):
        return db.query(
            Course.title,
            func.count(Transaction.id).label('sales'),
            func.sum(Transaction.amount).label('revenue')
        ).join(Transaction, Transaction.course_id == Course.id) \
         .filter(Transaction.status == 'completed') \
         .group_by(Course.id) \
         .order_by(func.sum(Transaction.amount).desc()) \
         .limit(limit).all()
