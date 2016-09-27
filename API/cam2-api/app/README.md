This directory holds all of the core application files. 

Mailers and Channels have no forseeable use in this API.

Jobs could be used in the future, but for now is empty.

Controllers house the actions that can be performed.  Each model has the following actions provided by the 'resources :{modelname}' line in config/routes.rb:
-Create
-Edit
-Destory
-index

If you want to create additional actions in a controller, you must write the action, then write a route that corresponds to that action in the routes.rb file.  If you do not, then you will have an error saying that no route corresponds with that action.  


Views are what the user sees as a result of actions.  In a Rails application with a front end, these views are most often HTML files with embedded Ruby (myfile.html.erb).  However, the API has no front end so it may seem strange we have views at all.  We need them though, because we build our json responses with jbuilder.  That gem will look for the specified files in the views directory.  That means if you want to build a response with jbuilder, you need to put a corresponding file in views folder.


Both controllers and views are version controlled through the URLs.  This is important so we do not break any applications relying on the functionality of previous versions of the API.  That means, IF YOU INTEND ON CREATING MAJOR CHANGES TO THE API, YOU MUST CREATE A NEW VERSION, AND PUT ALL NEW CONTROLLER AND VIEW FILES IN THAT NAMESPACE.  YOU MUST ALSO CREATE THE ROUTES FOR THAT NAMESPACE IN ROUTES.RB.

Models hold the validations for our database, and can also hold class functions.  They are essentially Ruby classes that inherit from ActiveModel.  Think about them as any other class, but each model has a table (or multiple tables) in the database.

 
