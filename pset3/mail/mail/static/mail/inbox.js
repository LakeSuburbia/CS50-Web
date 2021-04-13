document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").addEventListener("submit", send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;



  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

      for (let email of emails) {
        if (email.archived == false || mailbox != 'inbox') {
          
          const row = document.createElement('div')
          row.setAttribute("class", "row");
          const mailboxDiv = document.createElement('div')
          mailboxDiv.innerHTML += "From: " + email.sender + "<br />"
          + "Subject: " + email.subject + "<br />" 
          + email.timestamp + "<br />";

          if (email.read)
          {mailboxDiv.setAttribute("class", "col-sm mailbox border read border-light");}
          else
          {mailboxDiv.setAttribute("class", "col-sm mailbox border unread border-primary");}


          row.appendChild(mailboxDiv);
          mailboxDiv.addEventListener('click', () => load_email(email));

          if (mailbox == 'inbox' || mailbox == 'archive') {
            const archive = document.createElement('button');
            archive.setAttribute("class", " rounded-right col-sm button btn btn-danger");
            archive.textContent = email.archived ? "Unarchive" : "Archive";
            row.appendChild(archive);
            archive.addEventListener('click', () => {
              fetch('/emails/'+`${email.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    archived: !(email.archived)
                })
              }).then(() => load_mailbox(mailbox));
            });
          }

          document.querySelector('#emails-view').appendChild(row);

        }

      }
    });
  
}



function send_email(event){
  event.preventDefault();

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value,
    }),
  })
  .then(response => response.json())
  .then(result => {
    // Print result
    console.log(result);
  })
  .then(load_mailbox("sent"))
  .catch((error) => console.log(error));
}