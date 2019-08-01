import os

from flask import Flask, render_template, redirect, request, url_for

from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "kitty_task_manager"
app.config["MONGO_URI"] = 'mongodb+srv://KittyOwner:Stephbar2@kittysfirstcluster-f9urv.mongodb.net/kitty_task_manager?retryWrites=true&w=majority'

mongo = PyMongo(app)

# Route decorators

# Get all the tasks and display them
@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    
    # Redirect to tasks template, return all tasks. I'm sending tasks in twice as I cant make it iterate over tasks more than once
    return render_template("tasks.html", tasks=mongo.db.kitty_tasks.find())

# Add a task to the database
@app.route('/add_task')
def add_task():
    _categories = mongo.db.kitty_categories.find()
    category_list = [category for category in _categories]
    return render_template("addtask.html", categories = category_list)

# Insert the task when 'Add Task' is clicked. Invoked by 'form action="{{ url_for('insert_task') }}"'
@app.route('/insert_task', methods=['POST'])
def insert_task():
    # Access the tasks collection
    tasks = mongo.db.kitty_tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))
    
    
# Edit the task that has been selected for editing from the tasks.html
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.kitty_tasks.find_one({"_id": ObjectId(task_id)})
    all_categories = mongo.db.kitty_categories.find()
    return render_template('edittask.html', task=the_task, categories=all_categories)
    
# Update the editted task when 'Edit Task' is clicked. Invoked by 'form action="{{ url_for('update_task') }}"'
@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
     # Access the tasks collection
    tasks = mongo.db.kitty_tasks
    tasks.update({"_id": ObjectId(task_id)},
    {
        'task_name': request.form.get('task_name'),
        'category_name': request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent': request.form.get('is_urgent')
        
    })
    return redirect(url_for('get_tasks'))
    
# Delete the task when 'Done' is clicked. Invoked by 'href="{{ url_for('delete_task', task_id=task._id) }}"''
@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    # Access the tasks collection
    mongo.db.kitty_tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))
    
# Get categories function
@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories=mongo.db.kitty_categories.find())
    
# Template that allows us to add a new category
@app.route('/new_category')
def new_category():
    return render_template('addcategory.html')
    
    
# Edit categories function
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.kitty_categories.find_one({'_id':ObjectId(category_id)}))
    
# Update categories function
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.kitty_categories.update(
        {'_id':ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))
    
# Delete categories function
@app.route('/delete_category/<category_id>')
def delete_category(category_id):
        mongo.db.kitty_categories.remove({'_id':ObjectId(category_id)})
        return redirect(url_for('get_categories'))
        
# Insert the Category when 'Add Category' is clicked. Invoked by 'form action="{{ url_for('insert_category') }}"'
@app.route('/insert_category', methods=['POST'])
def insert_category():
    # Access the categories collection
    categories = mongo.db.kitty_categories
    category_doc = {'category_name': request.form.get('category_name')}
    categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))
    

    
    


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)
    
    