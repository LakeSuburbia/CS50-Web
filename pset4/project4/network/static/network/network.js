document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#allposts').addEventListener('click', () => load_posts('allposts'));
    document.querySelector('#network').addEventListener('click', () => load_posts('allposts'));
    document.querySelector('#following').addEventListener('click', () => load_mailbox('following'));
    document.querySelector('#profile').addEventListener('click', () => load_profile());
  
    // By default, load the inbox
    load_posts('allposts');
  });

  function load_profile() {
    // Show compose view and hide other views
    document.querySelector('#posts-view').style.display = 'none';
    document.querySelector('#profile-view').style.display = 'block';
  }

  function load_posts() {
    // Show compose view and hide other views
    document.querySelector('#profile-view').style.display = 'none';
    document.querySelector('#posts-view').style.display = 'block';
  }