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
  .catch((error) => console.log(error));
}




/*
function archive_email(email_id){
  fetch('/emails/', {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })
}
*/



/*
function get_mailbox(mailbox){
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
  
      // ... do something else with emails ...
      for (email in emails){
        var mail = document.createElement("div");
        var sender = document.createElement('h5');
        var sub = document.createElement('p');
        var time = document.createElement('p');
        var id = document.createElement('p');

        id.innerHTML = emails[email]['id'];
        id.style.display = 'none';
        if (emails[email]['read'] == true) {
          mail.style.backgroundColor = 'lightgray';
        }
        else {
          mail.style.backgroundColor = 'white';
        }
        mail.classList.add('container');
        mail.classList.add('mail');

        mail.addEventListener('click', () => load_email());
        sub.addEventListener('click', () => load_email());
        time.addEventListener('click', () => load_email());
        sender.addEventListener('click', () => load_email());
      }
  });
}
*/