document.addEventListener('DOMContentLoaded', function() {
    const follow = document.querySelector('#follow-btn');
    const user_name = document.querySelector('#usname').innerHTML;
    if (follow) {
        fetch(`/follow/${user_name}`)
        .then(response => response.json())
        .then(followw => {
            if (followw.follows === "True") {
                follow.innerHTML = `<button id="follower" class="btn btn-primary following">Unfollow</button>`
            }
            else {
                follow.innerHTML = `<button id="follower" class="btn btn-primary following">Follow</button>`
            }
            document.querySelector('#follower').addEventListener('click', () => change_following(user_name));
        });
    }
})


function change_following(user_name) {
    fetch(`/follow/${user_name}`, {
        method: 'PUT',
      })
        .then(response => response.json())
        .then(followw => {
            if (followw.follows === "True") {
                let followers = document.querySelector("#followers").innerHTML;
                followers++;
                document.querySelector("#followers").innerHTML = followers;
                document.querySelector("#follower").innerHTML = `Unfollow`;
            }
            else {
                let followers = document.querySelector("#followers").innerHTML;
                followers--;
                document.querySelector("#followers").innerHTML = followers;
                document.querySelector("#follower").innerHTML = `Follow`;
            }
        });
}
