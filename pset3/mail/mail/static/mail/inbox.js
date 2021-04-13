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
          
          // create a row to wrap the mail (+ archive button)
          const row = document.createElement('div')
          row.setAttribute("class", "row");

          // create a div for the mail preview itself
          const mailboxDiv = document.createElement('div')

          // styling for the mail preview
          if (email.read)
          {mailboxDiv.setAttribute("class", "col-sm mailbox border read border-light");}
          else
          {mailboxDiv.setAttribute("class", "col-sm mailbox border unread border-primary");}

          // Load the mail when you click the div
          mailboxDiv.addEventListener('click', () => load_email(email));

          // add the mailbox to the row
          row.appendChild(mailboxDiv);

          // We only need an archive button when we're in inbox or archive
          if (mailbox == 'inbox' || mailbox == 'archive') {
            // Create archive div
            const archive = document.createElement('button');
            // style archive div
            archive.setAttribute("class", "rounded-right col-sm button btn btn-danger");

            // decide wether you should archive or unarchive
            if (email.archived)
            {archive.textContent = "Unarchive"}
            else
            {archive.textContent = "Archive"}

            // add archive to the row
            row.appendChild(archive);

            // Create the archive / unarchive function
            archive.addEventListener('click', () => {
              fetch('/emails/'+`${email.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    archived: !(email.archived)
                })
              }).then(() => load_mailbox(mailbox));
            });
          }

          // Bring the row to the DOM
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