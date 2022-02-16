
from unicodedata import name
from flask import Flask, render_template, request, redirect, url_for
import os, json, re
from pym import * 
from azure.storage.blob import BlobServiceClient, PublicAccess

app = Flask(__name__)

print(os.getenv("PORT"))
port = int(os.getenv("PORT", 8000))


#cursor = connect.cursor()
print("Opened database successfully")

# retrieve all the users picture with file names and size and image loaded.
# search for a name and show his picture on the web
# display all pics where salary is < 1000 ------ focus on this tmrw
# add a pic for user
# add a user
# remove a user
# change keyword for a user
# change salary for a user


# default
@app.route('/', methods=["GET"])
def hello_world():
    return render_template('index.html', result={})


@app.route('/display_all_users', methods=["GET"])
def display():
    return render_template('display_all_users.html', jsonfile=readAllUsers())


@app.route('/add_a_pic_for_user', methods=["GET"])
def display_two():
    return render_template('display_all_users.html', jsonfile=readAllUsers())
   

# get the name and sizes of the file stored on cloud.
@app.route('/list_files', methods=["GET"])
def list_files():

    sql = "SELECT name,picture from people"
    cursor.execute(sql)
    output = cursor.fetchall()

    files_dict = {}
    files_list = os.listdir('./static/pics/')
    for file in files_list:
        file_name = './static/pics/' + file
        files_dict[file] = os.stat(file_name).st_size


    return render_template('list_files.html', result=files_dict)


@app.route('/search_sal', methods=["GET"])
def search_room():
    ret = []
    return render_template('salary_search.html', result=ret)


# search by name function
@app.route('/search_sal', methods=["POST"])
def search_by_room():
    sal_st = request.form["sal_start"]
    sal_end = request.form["sal_end"]
    if sal_st == '' and sal_end == '':
        sal_st = 0
        sal_end = 0
    if sal_st == '':
        sal_st = 0
    if sal_end == '':
        sal_end = 0
    cur = getCursor()
    cur.execute(
        'SELECT * FROM people WHERE Salary between %s and %s ', (sal_st, sal_end, ))
    result = cur.fetchall()
    print(json.dumps(result))
    return render_template('salary_search.html', jsonfile=result)


@app.route('/show_pic_by_name', methods=["GET"])
def show_pic():
    return render_template('show_pic_by_name.html')



##below two method's code taken from here : https://tomlogs.github.io/build-a-photos-application-with-azure-blob-storage
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING') # retrieve the connection string from the environment variable
container_name = "firstcontainer"#"photos" # container name in which images will be store in the storage account
#CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME')
blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # create a blob service client to interact with the storage account
#bbs = BlockBlobService(connect_str)
try:
    container_client = blob_service_client.get_container_client(container=container_name) # get container client to interact with the container in which images will be stored
    container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
except Exception as e:
    container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist

@app.route("/upload-photos", methods=["POST"])
def upload_photos():
    filenames = ""

    for file in request.files.getlist("photos"):
        try:
            container_client.upload_blob(file.filename, file) # upload the file to the container using the filename as the blob name
            filenames += file.filename + "<br /> "
        except Exception as e:
            print(e)
            print("Ignoring duplicate filenames") # ignore duplicate filenames
        
    return redirect('/view_photos')  

@app.route("/view_photos")
def view_photos():
    blob_items = container_client.list_blobs() # list all the blobs in the container

    img_html = "<div style='display: flex; justify-content: space-between; flex-wrap: wrap;'>"

    for blob in blob_items:
        blob_client = container_client.get_blob_client(blob=blob.name) # get blob client to interact with the blob and get blob url
        print(blob_client.url)
        size = blob.size/1000
        last_modified_ts =blob.last_modified
        print(str(size)+" "+str(last_modified_ts))
        #curr_blob = BlockBlobService.get_blob_properties(bbs,container_name,blob.name)
        #length = curr_blob.properties.content_length
        #print(length+" hey "+curr_blob)
        #print("now "+blob_client.size)
        img_html += "<img src='{}' width='auto' height='200' style='margin: 0.5em 0;'  />".format(blob_client.url) # get the blob url and append it to the html
  #<figcaption>"+blob.name+"</figcaption>  
    img_html += "</div>"

    # return the html with the images
    #return render_template('view_photos.html', result=result)
    return """
    <head>
    <!-- CSS only -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="/">Show Photos </a>
            </div>
        </nav>
        <a href="/">Go back to Home Page</a>
        <div class="container">
            <div class="card" style="margin: 1em 0; padding: 1em 0 0 0; align-items: center;">
                <h3>Upload new File</h3>
                <div class="form-group">
                    <form method="post" action="/upload-photos" 
                        enctype="multipart/form-data">
                        <div style="display: flex;">
                            <input type="file" accept=".png, .jpeg, .jpg, .gif" name="photos" multiple class="form-control" style="margin-right: 1em;">
                            <input type="submit" class="btn btn-primary">
                        </div>
                    </form>
                </div> 
            </div>
        
    """ + img_html +"</div></body>"


# search by name function
@app.route('/show_pic_by_name', methods=["POST"])
def show_pic_name():
    username = request.form["username"]
    print(username)
    #cursor = getCursor()
    res = getPicbyName(username)
    
    pictureName =  res[2:len(res)-3]
    print(pictureName)
    blob_items = container_client.list_blobs()
    print("==== " + str(blob_items))
    for blob in blob_items:
        print("index "+str(blob.name))

        if str(blob.name) == str(pictureName):
            blob_client = container_client.get_blob_client(blob=blob.name) # get blob client to interact with the blob and get blob url
            print("hey")
            url = str(blob_client.url)
            size = str(blob.size/1000)
            print("-------"+str(url)+" "+str(size))
            break
    
    
    return render_template('show_pic_by_name.html',pictureName=pictureName, username=username,url=url,size=size )

@app.route('/update', methods=["GET"])
def update_by_room():
   
    cur = getCursor()
    cur.execute(
        'SELECT Name, Salary, Keywords FROM people where Name is Not Null')
    result = cur.fetchall()

    return render_template('update.html', result=result)


@app.route('/update', methods=["POST"])
def update():
    name = request.form.get('opt')
    salary = request.form["salary"]
    keywords = request.form["keywords"]
    cur = getCursor()
    if salary != '' and keywords != '':
        sql = 'UPDATE people SET Keywords =%s, Salary =%s WHERE Name = %s'
        cur.execute(sql, (keywords,salary,name))
    if salary != '':
        cur.execute(
            'UPDATE people SET Salary = %s WHERE Name = %s', (salary, name))
    if keywords != '':
        cur.execute(
            'UPDATE people SET Keywords = %s WHERE Name = %s', (keywords, name))
    conn.commit()
    return render_template('index.html')


@app.route('/list', methods=["GET"])
def just_hello():
    cur = conn.cursor()
    sql = "SELECT Name, Salary, Keywords FROM people where Name is Not Null;"
    cur.execute(sql)
    result = cur.fetchall()
    return render_template('update.html', result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

@app.route('/display_all_users', methods=["GET"])
def display_you():
    #name, picture, salary, room, telnum, keywords
    name = []
    picture = []
    salary = []
    room = []
    telnum = []
    keywords = []
    pictureName = []

    allusers = readAllUsers()

    for row in allusers:
        name.append(allusers[0])
        salary.append(allusers[1])
        pictureName.append(allusers[4])
        room.append(allusers[2])
        telnum.append(allusers[3])
        keywords.append(allusers[5])
        
        if(allusers[4]):
            picture.append(allusers[4]) #get picture from storage
        else:
            picture.append(" ") #nothing

    userslist = zip(name, pictureName, salary,room,
                   telnum, keywords, picture)

    #print(json.dumps(userslist,indent=3))
    print(json.dumps(allusers))
    #return userslist

    return render_template('display_all_users.html', jsonfile=allusers) 
    #jsonfile=json.dumps(userslist))