## Functional Requirements
1. Sign In
2. Sign out
3. Register an account
4. Create Folders
5. Edit notes
6. Export Notes
7. Attach Images
8. Search notes by note names
9. Delete user profile
10. Search with advanced expressions
11. Connect to Google Translate API
12. Edit user profile
13. Create Tables with Links to Notes
14. Delete Notes

# UI Sketch with Functionals
1. [Account Page](images/ui1.png)
2. [Delete User Page](images/ui2.png)
3. [Edit Note Page](images/ui3.png)
4. [Edit Table Page](images/ui4.png)
5. [Edit User Profile Page](images/ui5.png)
6. [Index Page](images/ui6.png)
7. [Register Account Page](images/ui7.png)

## Non-functional Requirements
1. Only work expect to work Google Chrome
2. Multilingual Support
3. Dark mode
4. Change font colors


Yousef Asad

**1. Sign in**

- **Summary:**
This use case outlines the steps a User follows to sign in to the Notes Application, allowing them to access their personalized notes, settings, and other features.
- **Actors:**
User and Notes Application
- **Pre-condition:**
User has the app installed and loaded to sign in page
- **Trigger:**
User clicks sign in button on apps login page
- **Primary Sequence:**
1. The Notes Application displays the sign-in interface, prompting the User to enter their username and password.
2. The User enters their registered email address and password
3. The Notes Application validates the entered information by verifying it against the stored database.
4. If the entered credentials are valid, the User is logged in
- **Primary Postconditions:**
User Logs in, the User is signed in and can access their stored notes, preferences, and other personalized features within the Notes Application.
User is not logged in, User is stuck at login page.
- **Alternate Sequence:**
- Invalid Password
    1. User inputs invalid password
    2. Systems prompts forgot password option
    3. System sends link to email with password recovery tool
- **Alternate Sequence:**
User has not registered an account yet
    1. Select the "Sign Up" option to create a new account.
    2. Input credentials


Yousef Asad

**2. Sign Out**

- **Summary:**
This use case outlines the steps a User follows to sign out of the Notes Application, allowing them to exit their session.
- **Actors:**
User and Notes Application
- **Pre-condition:**
The User has the Notes Application installed and is currently logged in, viewing the application's interface.
- **Trigger:**
User clicks sign out button
- **Primary Sequence:**
1. Pop up prompts if user wants to sign out
2. User clicks sign out
3. App redirects user to sign in page
- **Primary Postconditions:**
User is signed out, the User is redirected to sign in page.
User not signed out, user remains on page where they had been last.
- **Alternate Sequence :**
User Cancels signout procedure
    1. Sign out window closes
    2. System displays page where user was


Yousef Asad

**3.  Register an account**

- **Summary:**
This use case outlines the steps a User follows to register an account on the notes app
- **Actors:**
  User and Notes Application
- **Pre-condition:**
User has the app installed and loaded to sign in page
- **Trigger:**
User clicks register account button
- **Primary Sequence:**
1. User clicks register account
2. System opens new registration page
3. System Prompts user to enter personal information
4. User clicks register account
5. App redirects user to sign in page
6. User signs in with credentials
- **Primary Postconditions:**
User is signed in with newly registered account, the User is redirected to home page.
User is not registered, User remains on signup page.
- **Alternate Sequence :**
User input Email that is already in use
    1. App displays error to user
    2. Prompts user to login with email or use different


Yousef Asad

**4.  Create Folders**

- **Summary:**
This use case outlines how Users can organize their notes using a folder system directly on the home page of the Notes Application
- **Actors:**
User and Notes Application
- **Pre-condition:** The User has the Notes Application installed and is on the home page
- **Trigger:** User clicks on homepage
- **Primary Sequence:**
1. User creates folder and names it
2. User drags or uploads notes in specified folder
3. User toggles through different folders on home menu
- **Primary Postconditions:**
The User can efficiently organize their notes, using a folder system on the home page, enhancing their ability to categorize and navigate their content effectively.
User does not change anything on home layout, user home page remains the same.
- **Alternate Sequence :**
User does not change home layout
    1. Home page remains organized in a standard grid or list format.


Noah Nguyen

**5.  Edit Notes**

-**Summary:**
The current user on the webpage can click on and edit a selected note
- **Actor(s):**
The login user
- **Pre-condition:**
User at homepage; page opened via notes list
- **Trigger:**
User clicks on the edit button
- **Primary Sequence:**
1. Program checks which name of notes that is selected
2. Program opens up Edit Notes page for editing content in note
3. A box of existing content is shown on the page
4. The user enters content or deletes content in the box
5. The user selects “save” button and exits page
- **Primary Postconditions:**
User has edited and saved content within named note
- **Alternate Sequence:**
User creates changes without saving
    1. User opens note page
    2. User edits content within box by adding or deleting content
    3. User exits the Edit Note page
    4. No content changes are saved to the note


Noah Nguyen

**6.  Export Notes**

-**Summary:**
The user can download a note in the file type version based on their choice
- **Actor(s):**
The login user
- **Pre-condition:**
User at Edit Notes Page
- **Trigger:**
User hits the “Export” button
- **Primary Sequence:**
1. Program opens up pop-up for user
2. Pop-up contains the question “What type of file?” with choices of file types
3. User selects their file type
4. User clicks download button on pop-up
5. File is downloaded to the user’s machine
6. Pop-up is removed from the page
- **Primary Postconditions:**
User downloads page as preferred file type
- **Alternate Sequence:**
User leaves “Export” pop-up
    1. User selects “Back” button on pop-up
    2. Pop-up taken off web page
    3. User remains in Edit Note Page


Noah Nguyen

**7.  Attach Images**

**Summary:**
The user can attach images to their notes with
- **Actor(s):**
The login user
- **Pre-condition:**
User is at Edit Note page
- **Trigger:**
User clicks on the “Attach Images” button
- **Primary Sequence:**
1. Program will prompt a file explorer
2. User select image from files
3. User will select a “Done” button
4. Program will display attachment link of chosen image
- **Primary Postconditions:**
An attachment is placed on a note
- **Alternate Sequence:**
User cancels “Attach Images” button 
    1. Program brings up file explorer 
    2. User hits “Cancel” button on file explorer
    3. File explorer pop-up removed, web goes back to Edit Note page


Nutthawat Panyangnoi

**8.  Search notes by note names**

- **Summary:**
This use case  allows user to search for specific note names.
- **Actor(s):**
User, note’s user
- **Pre-condition:**
 User must already registered and have an account. Once user logged in they will be able to see the search box.
- **Trigger:**
User click on Search box and fill up search box with specific note name.
- **Primary Sequence:**
1. User finished registration and logged in to the website.
2. The search box appeared on top the profile page to search file from existed note files.
3. User enter “String”name of the notes that they look for and click search or just press “Enter” on keyboard.
4. The web application will traverse and search for the existing notes in the profile.
5. If the string text that user entered is found. The webpage will retrieve and show that specific note to the user.
- **Primary Postconditions:**
The webpage will show all files that matched to the search text that user entered. If multiple notes have similar name contained ,all of notes will appeared for user to select.
- **Alternate Sequence:**
User does not have an account
    1. user unable to logged in and see the search bar.
- **Alternate Sequence:**
User profile does not have any notes. 
    1. Use will not see any file after entering the search box.
- **Alternate Sequence:**
There are multiple files existing but none of the files matched to the search text.
    1.Text appearing “File is not found!”


Nutthawat Panyangnoi

**9.  Delete user profile**

- **Summary:**
This use case allow user to delete their own account from the our Note’ Website.
- **Actor(s):**
 User, Note’s User
- **Pre-condition:**
User must fully finish registration an account or User must have an account already. User must click on User click on Edit User profile.
- **Trigger:**
 User click on Edit User Profile. The delete account button appeared. User click on “Delete Account button”
- **Primary Sequence:**
1. User logged in to the webpage profile .
2. User click on profile name.
3. User select Edit User Account under profile name.
4. The delete account button appeared at the bottom of user edit profile page.
5. User click on “Delete Account”.
6. The webpage will forward to new webpage call “Delete Account” with message prompt the reason why user delete the account with another prompt message ask user to enter their password.
7. After user fill up the prompt message and entered their password and click delete.
8. The web application will prompt the message to confirmation of deleting account “Are u sure you want to delete an account?”.
9. User will have to click on Button “Yes”, web application will execute a command remove an user account from database of the server.
- **Primary Postconditions:**
User finished remove their account. The prompt appear “Account successfully removed!”, the webpage redirect to homepage of the website.
- **Alternate Sequence:**
User cancelling deletion profile.
    1.User select edit User Account, types in their password 
    2.They hit the confirmation button of delete profileT
    3.he system prompts the user with ‘Yes’ or ‘No’ message to confirm deletion.
    4.User selects “No”
    5.The account remains unchanged. 
    6.User is redirected to the homepage.



Nutthawat Panyangnoi

**10.  Search with advanced expressions**

- **Summary:**
This use case allow user to search the file with expression at the specific location in the existing file. This search will allow to search the contents that match inside the file.
- **Actor(s):**
User, Note’s User
- **Pre-condition:**
User must already registered and have an account. When user logged in, they will be able to see search bar.
- **Trigger:**
User click on Search box and fill up search box with specific note name and user click on “Filter Search” button.
- **Primary Sequence:**
1. The search box will appear on top the profile page to search file from existed note files, user can allow to enter any text with a special expression.
2. User enter name of the notes with any expression that they look for and click on Filter Search button
3. The drop boxes will displaying specifically existing catalogs/folder file.
4. The catalog/folder files will show check box.
5. User can click on check box to make a specific search inside those check box.
6. User enters the word(s) in the search box
7. Files with the word(s) will appear on the user profile.
- **Primary Postconditions:**
The webpage will show all files that matched to the expression and string that user enter in search text that user entered. If multiple notes have similar name contained ,all of notes will appeared for user to select. User be able to click on the notes and see the contents.
- **Alternate Sequence:**
User does not have an account
    1.user unable to logged in and see the search bar.
- **Alternate Sequence:**
User profile does not have any notes. 
    1.Use will not see any file after entering the search box.
 

Meghana Indukuri

**11.  Connect to Google Translate API**

- **Summary:**
Users should be able to convert their notes from one language to another. The application should utilize the google translate API so the user can do so.
- **Actors:**
    	User and Notes Application
- **Pre-condition:**
User is at the edit notes page
- **Trigger:**
User clicks translate button located on the edits note page
- **Primary Sequence:**
1. System prompts the user to select the language to translate the note to.
2. User clicks on the language they would like to translate the note to.
3. System utilizes the google translate API.
4. Google translate API translates the text in the note, and sends it back to the application
5. The text is then translated using the information provided by the google translate API.
6. The user can then save the note with the translated text.
- **Primary Postconditions:**
The note will have the translated text saved, and when the user decides to edit it again, only the translated text will be shown. User will return to the homepage
- **Alternate Sequence:**
- User does not save changes to the note after translation
    1. System prompts the user to select the language to translate the note to.
    2. User clicks on a language
    3. System utilizes the google translate API.
    4. Google translate API translates the text in the note, and sends it back to the application
    5. The text is then translated using the information provided by the google translate API.
    6. The user decides not to the save the note with the translated text
    7. The text is not saved, and the user returns back to the homepage

- **Alternate Sequence :**
User tries to translate note from a language to the same language
    1. System prompts user to select the language to translate the note to
    2. User selects a language the note is already written in.
    3. System utilizes the google translate API.
    4. Google translate API, makes no translation and informs the application of no new text
    5. The application makes no changes to the text
    6. The user has no new text to save


Meghana Indukuri

**12.  Edit User Profile**

- **Summary:**
Users should be able to edit their user profile, to change their password, name or username.
- **Actors:**
User and Notes Application
- **Pre-condition:**
User is at the edit user webpage and has an account
- **Trigger:**
User clicks change password,username or name option located on the edit user webpage.
- **Primary Sequence:**
1. User selects which of their personal information they would like to modify.
2. User gets prompted with a textbox to change to a new username, password or name
3. User must enter their new username,password or name in the textbox
4. User must repeat their new username,password or name in the textbox
5. Application prompts the user with an “are you sure?” message
6. User clicks yes
7. User’s username, password or name is permanently modified
- **Primary Postconditions:**
User has a new username, password or name after the modification. Users must use the new username, password or name whenever they sign in from this point forward.
- **Alternate Sequence:**

User tries to change existing personal information with the same information
1. User selects which of their personal information they would like to modify
2. User gets prompted with a textbox to change to a new username, password or name
3. User enters the same username, password or name as the existing ones
    1. Application prompts user with an invalid password message
    2. User can enter a new password, username or name in the textbox
- **Alternate Sequence :**
User decides to not change information
    1. User selects which of their personal information they would like to modify.
    2. User gets prompted with a textbox to change to a new username, password or name
    3. User must enter their new username,password or name in the textbox
    4. User must repeat their new username,password or name in the textbox
    5. Application prompts the user with an “are you sure?” message
    6. User clicks no
    7. No changes are made to the user’s name, username or password


Meghana Indukuri

**13.  Create Tables with Links to Notes**

- **Summary:**
Users should be able to create tables in the application that contain links to existing notes in their account on the application.
- **Actors:**
User and Notes Application
- **Pre-condition:**
User is at the tables webpage in the application
- **Trigger:**
User clicks create table in the tables webpage
- **Primary Sequence:**
1. Web application prompts user to enter number of rows and columns
2. User selects wanted rows and columns
3. Empty Table is created by web application
4. User can type in the cells of the table
5. User selects links of existing notes from the side of the webpage
6. Selected links are inserted into the cells of the table by the user
7. The table is then be saved by the user
- **Primary Postconditions:**
User has a new table that is saved with the information they added while editing the table. The table contains links to notes from their accounts that they have written before.
- **Alternate Sequence:**
- User enters invalid rows and columns for each table creation
    1. Web application prompts user to enter number of rows and columns
    2. User enters invalid row and column values
    3. Web application displays an error message
    4. User is prompted to enter correct row and column values
- **Alternate Sequence :**
User creates table with no note links
    1. Web application prompts user to enter number of rows and columns
    2. User selects wanted rows and columns
    3. Empty Table is created by web application
    4. User saves empty table
    5. Table is saved to the application under the user's account, but is empty containing no links to any existing notes.


Meghana Indukuri

**14.  Delete Notes**

- **Summary:**
Users should be able to delete their existing notes
- **Actors:**
User and Notes Application
- **Pre-condition:**
User is at the edit note webpage of the application
- **Trigger:**
User clicks on the delete button located on the edit note webpage.
- **Primary Sequence:**
1. System prompts user to with message asking to confirm deletion, with options yes or no
2. User selects yes
3. Note content is deleted by application
4. User is returned to homepage
5. Application no longer displays deleted note on homepage
- **Primary Postconditions:**
Note is permanently removed from the user's account and cannot be retrieved.
- **Alternate Sequence:**
User decides to not delete note
    1. System prompts user to with message asking to confirm deletion, with options yes or no
    2. User selects no from prompt
    3. User remains on edit note webpage
    4. Note remains unchanged and not deleted


