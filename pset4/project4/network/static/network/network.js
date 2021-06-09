document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#allposts').addEventListener('click', () => load_posts('allposts'));
    document.querySelector('#network').addEventListener('click', () => load_posts('allposts'));
    document.querySelector('#following').addEventListener('click', () => load_posts('following'));
    document.querySelector('#profile').addEventListener('click', () => load_profile('myProfile'));
  
    // By default, load the inbox
    load_posts('allposts');
  });

  function load_profile(user) {
    // Show compose view and hide other views
    document.querySelector('#profile-view').style.display = 'block';
    document.querySelector('#posts-view').style.display = 'block';
    
    
    if (user == 'myProfile')
    {
        document.querySelector('#new-post').style.display = 'block';
        fetch(`/get_currentuser`)
        .then (response => response.json())
        .then(data => {
            console.log(data.userid)
            console.log(data.username)
            header = document.createElement('h2')
            header.textContent = data.username;
            document.querySelector('#username').innerHTML=header
            fetch(`/get_followcount/${data.userid}`)
            .then(response => response.json())
            .then(data => {
                
                console.log(data.followers)
                console.log(data.following)

                followers = document.createElement('b')
                followers.textContent = "Followers: "
                followers.textContent += data.followers

                following = document.createElement('b')
                followers.textContent = "Following: "
                following.textContent = data.following
                
                document.querySelector('#followcount').innerHTML=following
                document.querySelector('#followercount').innerHTML=followers
            })
        })
    }
    else{
        fetch(`/get_currentuser`)
        .then (response => response.json())
        .then(data => {
            if(data.userid == user.id)
            {
                load_profile('myProfile')
            }
            else{
                document.querySelector('#new-post').style.display = 'none';
                header = document.createElement('h2')
                header.textContent = data.username;
                document.querySelector('#username').innerHTML=header

                fetch(`/get_followcount/${user}`)
                .then(response => json(response))
                .then(followers => {
                    document.querySelector('followers').innerHTML=followers
                })
                .then(following => {
                    document.querySelector('following').innerHTML=following
                })
            }
        })
    }
  }
    


  function load_posts(postquery) {
    // Show compose view and hide other views
    document.querySelector('#profile-view').style.display = 'none';
    document.querySelector('#posts-view').style.display = 'block';

    query = ""
    
    if (postquery == 'allposts')
    {
        document.querySelector('#new-post').style.display = 'block';
    }
    else{
        document.querySelector('#new-post').style.display = 'none';
        query+="/"+postquery;
    }

    fetch(`/posts${query}`)
      .then(response => response.json())
      .then(posts => {
        // Only for debugging purposes 
        console.log(posts);

        for (let post of posts) {
          
            const row = document.createElement('div')
            row.setAttribute("class", "col post");

            // create a div for the mail preview itself
            
            row.innerHTML += "<a href=''><h4>" + post.poster + "</h4></a> <p>"
            + post.body + "</p> <p class='timestamp'>" 
            + post.timestamp + "</p> ";


            // Bring the row to the DOM
            document.querySelector('#posts-view').appendChild(row);
        }
      });



  }