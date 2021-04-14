document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  //document.querySelector('#replyButton').addEventListener('submit', (mail) => compose_email);
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").addEventListener("submit", send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(mail) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  if (mail.sender != undefined)
  {
    document.querySelector('#compose-recipients').value = mail.sender;
    document.querySelector('#compose-subject').value = mail.subject;
    document.querySelector('#compose-body').value = "\n\non " + mail.timestamp + " " + mail.sender + " wrote: \n\n" + mail.body;
  }
  else{
    // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  }
  
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  if (mailbox == 'inbox' || mailbox == 'sent' || mailbox == 'archive')
  {
    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    fetch(`/emails/${mailbox}`)
      .then(response => response.json())
      .then(emails => {
        // Only for debugging purposes 
        console.log(emails);

        for (let email of emails) {
          
            if (email.archived == false || mailbox != 'inbox') {
              
              // create a row to wrap the mail (+ archive button)
              const row = document.createElement('div')
              row.setAttribute("class", "row");

              // create a div for the mail preview itself
              const mailDiv = document.createElement('div')
              mailDiv.innerHTML += "From: " + email.sender + "<br />"
              + "Subject: " + email.subject + "<br />" 
              + email.timestamp + "<br />";

              // styling for the mail preview
              if (email.read)
              {mailDiv.setAttribute("class", "col-sm mailbox border read border-light");}
              else
              {mailDiv.setAttribute("class", "col-sm mailbox border unread border-primary");}

              // Load the mail when you click the div
              mailDiv.addEventListener('click', () => load_mailbox(email));

              // add the mailbox to the row
              row.appendChild(mailDiv);

              // We only need an archive button when we're in inbox or archive
              if (mailbox == 'inbox' || mailbox == 'archive') {
                // Create archive div
                const archive = document.createElement('button');
                // style archive div
                archive.setAttribute("class", "rounded-right col-sm archiveButton btn btn-danger");

                // decide wether you should archive or unarchive
                if (email.archived)
                {archive.textContent = "Unarchive"}
                else
                {archive.textContent = "Archive"}

                // add archive to the row
                row.appendChild(archive);

                // Create the archive / unarchive function
                archive.addEventListener('click', () => {
                  fetch(`/emails/${email.id}`, {
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
  else{
    email = mailbox;

    document.querySelector('#emails-view').innerHTML = `<h3>${email.subject}</h3>`;

    // Mark the mail as read
    fetch(`/emails/${email.id}`,{
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })

    // Push the mail to the DOM
    const mailContainer = document.createElement('div')
    const mailDiv = document.createElement('div')
    const replyDiv = document.createElement('div')

    mailDiv.setAttribute("class", "row mail border unread border-light");
    replyDiv.setAttribute("class", "rounded-bottom row replyButton btn btn-danger");

    mailDiv.innerHTML = 
    `From: ${email.sender} <br/>
    Subject: ${email.subject} <br/>
    ${email.timestamp} <br/>
    ${email.body}`


    replyDiv.innerHTML = "REPLY"
    replyDiv.addEventListener('click', () => compose_email(email));


    mailContainer.appendChild(mailDiv)
    mailContainer.appendChild(replyDiv)

    document.querySelector('#emails-view').appendChild(mailContainer);
    
    
  }
}



function send_email(event){
  event.preventDefault();

  // Call API with mail-content in jason format
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
    // Only for debugging purposes
    console.log(result);
  })
  .then(load_mailbox("sent"))
  .catch((error) => console.log(error));
}