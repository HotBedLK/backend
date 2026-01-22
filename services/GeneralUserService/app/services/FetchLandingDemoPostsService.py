from services.GeneralUserService.app.db.transaction import  Transactions



#service layer for get 12 random posts from the database
def FetchLandingDemoPostsService(db):
    #call repo layer and get 12 posts
    return Transactions.FetchLandingDemoPostsRepoFunc(db=db,limit=12)