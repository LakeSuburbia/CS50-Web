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
    .then(window.location.reload())
    .then(response => response.json())
    .then(emails => {

      for (email in emails) {
        if (email.archived == false || mailbox != 'inbox') {
          const div = document.createElement('div').innerHTML 
          += "From: " + email.sender + "<br />"
          + "Subject: " + email.subject + "<br />"
          + email.timestamp + "<br />";

          document.querySelector('#emails-view').appendChild(emailDiv);
          emailDiv.addEventListener('click', () => load_email(email));

          if (mailbox == 'inbox' || mailbox == 'archive') {
            
            const button = document.createElement('button');
            button.textContent = email.archived ? "Unarchive" : "Archive";

            document.querySelector('#emails-view').appendChild(button);
            button.addEventListener('click', () => {
              fetch('/emails/'+`${email.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    archived: !(email.archived)
                })
              }).then(() => load_mailbox(mailbox));
            });
          }

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