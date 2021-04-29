var entries = [];
var editId = null;
var createdDate = null;

var loginPage = document.querySelector('#login');
var basePage = document.querySelector('#journal');

var switchToLoginButton = document.querySelector('#switch-to-login');
var switchToSignupButton = document.querySelector('#switch-to-signup');
var fNameField = document.querySelector('#fNameEntry');
var lNameField = document.querySelector('#lNameEntry');
var loginButton = document.querySelector('#loginButton');
var signupButton = document.querySelector('#signupButton');
var authenticationHeader = document.querySelector('#login-header');
var emailField = document.querySelector('#email');
var passwordField = document.querySelector('#password');
var errorMessage = document.querySelector('#error-message');

switchToLoginButton.onclick = function() {
    fNameField.style.display = 'none';
    lNameField.style.display = 'none';
    switchToLoginButton.style.display = 'none';
    switchToSignupButton.style.display = 'inline';
    signupButton.style.display = 'none';
    loginButton.style.display = 'inline';
    authenticationHeader.innerHTML = 'LOGIN';
    errorMessage.style.display = 'none';
}

switchToSignupButton.onclick = function() {
    fNameField.style.display = 'block';
    lNameField.style.display = 'block';
    switchToLoginButton.style.display = 'inline';
    switchToSignupButton.style.display = 'none';
    signupButton.style.display = 'inline';
    loginButton.style.display = 'none';
    authenticationHeader.innerHTML = 'SIGN UP';
    errorMessage.style.display = 'none';
}

loginButton.onclick = function () {
    var email = emailField.value;
    var password = passwordField.value;

    if (email == '' | password == ''){
        errorMessage.style.display = 'block';
    } else {
        var data = 'email=' + email;
        data += '&password=' + password;

        fetch("http://localhost:8080/sessions", {
            method: 'POST',
            credentials:'include',
            body: data,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }).then(function(response){
            if(response.status == 401){
                errorMessage.innerHTML = 'Email or Password is Incorrect';
                errorMessage.style.display = 'block';
            } else if(response.status == 201) {
                switch_to_logged_in();
                loadLogsFromServer();
            }
        })
    }
}

function switch_to_logged_in(){
    loginPage.style.display = 'none';
    basePage.style.display = 'block';
}

function switch_to_logged_out() {
    basePage.style.display = 'none';
    loginPage.style.display = 'block';
}

signupButton.onclick = function () {
    var fname = fNameField.value;
    var lname = lNameField.value;
    var email = emailField.value;
    var password = passwordField.value;

    if (fname == '' | lname == '' | email == '' | password == ''){
        errorMessage.style.display = 'block';
    }
    else {
        var data = 'f_name=' + fname;
        data += '&l_name=' + lname;
        data += '&email=' + email;
        data += '&password=' + password;

        fetch("http://localhost:8080/users", {
            method: 'POST',
            body: data,
            credentials:'include',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }).then(function(response){
            if(response.status == 422){
                errorMessage.innerHTML = 'Email Already in Use, Try Again';
                errorMessage.style.display = 'block';
            }
            else {
                switch_to_logged_in();
            }
        })
    }
}

function postLog(data) {
    fetch("http://localhost:8080/logs", {
        method: 'POST',
        credentials:'include',
        body: data,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(function (response) {
        if(response.status == 401){
            switch_to_logged_out()
        } else {
            loadLogsFromServer();
        }
    });
}

function putLog(data) {
    fetch('http://localhost:8080/logs/' + editId, {
        method: 'PUT',
        body: data,
        credentials:'include',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(function (response) {
        if(response.status == 401){
            switch_to_logged_out()
        } else {
            loadLogsFromServer();
        }
    });
}

var addButton = document.querySelector('#add-Button');
addButton.onclick = addLog;

function addLog() {
    var headingContent = document.querySelector('#logHeading').value;
    var date = new Date();
    var dateContent = (date.getMonth()+1)+'-'+date.getDate()+'-'+date.getFullYear();
    var entryContent = document.getElementById('myTextArea').value;
    var ratingContent = document.querySelector('#logRating').value;
    var placeContent = document.querySelector('#logPlace').value;

    if( createdDate != null){
        if('C:' == createdDate.slice(0,2)){
            dateContent = createdDate + ' E:' + dateContent;
        } else {
            dateContent = 'C:' + createdDate + ' E:' + dateContent;
        }
    }

    if (headingContent == ''){
        headingContent = null;
    }
    if (entryContent == ''){
        entryContent = null;
    }
    if (ratingContent == ''){
        ratingContent = 0;
    }
    if (placeContent == ''){
        placeContent = null;
    }

    var data = "heading=" + encodeURIComponent(headingContent);
    data += "&rating=" + encodeURIComponent(ratingContent);
    data += "&date=" + encodeURIComponent(dateContent);
    data += "&entry=" + encodeURIComponent(entryContent);
    data += "&date=" + encodeURIComponent(dateContent);
    data += "&place=" + encodeURIComponent(placeContent);

    document.getElementById('myTextArea').value = '';
    document.querySelector('#logHeading').value = '';
    document.querySelector('#logRating').value = '';
    document.querySelector('#logPlace').value = '';

    if(createdDate == null){
        postLog(data);
    }
    else {
        createdDate = null;
        putLog(data);
    }
}




function deleteLogFromServer(logId){
    fetch('http://localhost:8080/logs/' + logId, {
        method: 'DELETE',
        credentials:'include',
    }).then(function(response){
        if(response.status == 401){
            switch_to_logged_out()
        } else {
            loadLogsFromServer();
        }
    });
};

//loads one log after edit button is pressed returns log dict
function loadOneLogFromServer(){
    fetch("http://localhost:8080/logs/" + editId, {
        credentials:'include',
    }).then(function (response){
        if(response.status == 401){
            switch_to_logged_out()
        } else {
            response.json().then(function (log) {
            showEdits(log);
        });
        }
        /*
        response.json().then(function (log) {
            showEdits(log);
        });
        */
    });
}

function showEdits(editLogDict) {
    var addButton = document.querySelector('#add-Button');
    addButton.style.display = 'none';
    var saveButton = document.querySelector('#save-button');
    saveButton.style.display = 'block';

    var logHeading = document.querySelector('#logHeading');
    var logRating = document.querySelector('#logRating');
    var logEntry= document.querySelector('#myTextArea');
    var logPlace = document.querySelector('#logPlace');

    logHeading.value = editLogDict.heading;
    if(editLogDict.rating != 'null'){
        logRating.value = editLogDict.rating;
    } else {
        logRating.value = 0;
    }
    logEntry.value = editLogDict.entry;
    logPlace.value = editLogDict.place;
    createdDate = editLogDict.date;
}

function addEdits() {
    var saveButton = document.querySelector('#save-button');
    saveButton.onclick = addLog;
}



function loadLogsFromServer(){
    fetch("http://localhost:8080/logs", {
       credentials: 'include',
    }).then(function (response) {
        if (response.status == 401){
            switch_to_logged_out();
        } else if ( response.status == 200){
            switch_to_logged_in();
            response.json().then(function (data) {
                logs = data;
                var list = document.querySelector("#my-log")
                list.innerHTML = "";
                var saveButton = document.querySelector('#save-button');
                var addButton = document.querySelector('#add-Button');
                saveButton.style.display = 'none';
                addButton.style.display = 'block';

                logs.forEach(function(log){
                    var newLog = document.createElement("li");
                    newLog.classList.add('log-entry')

                    var deleteButton = document.createElement('button');
                    deleteButton.id = 'delete-button';
                    deleteButton.innerHTML = 'X';
                    deleteButton.onclick = function () {
                        if(confirm('Delete ' + log.heading + '?')){
                            deleteLogFromServer(log.id);
                        }
                    }
                    newLog.appendChild(deleteButton);

                    var ratingDiv = document.createElement('div');
                    ratingDiv.classList.add('rating-display');
                    ratingDiv.innerHTML = log.rating;
                    newLog.appendChild(ratingDiv);

                    var headingDiv = document.createElement('div');
                    headingDiv.classList.add('heading-display');
                    headingDiv.innerHTML = log.heading;
                    newLog.appendChild(headingDiv);

                    var entryDiv = document.createElement('div');
                    entryDiv.classList.add('entry-display');
                    entryDiv.innerHTML = log.entry;
                    newLog.appendChild(entryDiv);

                    var placeDiv = document.createElement('div');
                    placeDiv.classList.add('place-display');
                    placeDiv.innerHTML = log.place;
                    newLog.appendChild(placeDiv);

                    var dateDiv = document.createElement('div');
                    dateDiv.classList.add('date-display');
                    dateDiv.innerHTML = log.date;
                    newLog.appendChild(dateDiv);

                    var editButton = document.createElement('button');
                    editButton.id = 'edit-button';
                    editButton.innerHTML = 'EDIT'
                    editButton.onclick = function () {
                        editId = log.id;
                        //2.Show any inputs and/or buttons for editing
                        loadOneLogFromServer();
                        //3.assign input values to the restaurant data
                        var saveButton = document.querySelector('#save-button');
                        saveButton.onclick = addLog;
                    }
                    newLog.appendChild(editButton);

                    list.appendChild(newLog);
                });

            });
        }
    });
}

loadLogsFromServer();
