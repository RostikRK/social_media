function edit_post(post_id, username) {
    fetch(`/post/${username}/${post_id}`)
        .then(response => response.json())
        .then(post => {
            document.querySelector(`#content-textarea-${post_id}`).innerHTML = post.content;
        });
    document.querySelector(`#edit-btn-${post_id}`).style.display = 'none';
    document.querySelector(`#content-show-${post_id}`).style.display = 'none';
    document.querySelector(`#content-edit-${post_id}`).style.display = 'block';
}

function save_post(post_id, username) {
    const content = document.querySelector(`#content-textarea-${post_id}`).value;
    console.log(content);
    fetch(`/post/${username}/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            new_content: content
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
    });
    document.querySelector(`#content-show-${post_id}`).innerHTML = content;
    document.querySelector(`#edit-btn-${post_id}`).style.display = 'block';
    document.querySelector(`#content-show-${post_id}`).style.display = 'block';
    document.querySelector(`#content-edit-${post_id}`).style.display = 'none';
}

function like(post_id, username) {
    const icon = document.querySelector(`#like-button-${post_id}`).innerHTML;
    var action = "Remove";
    if (icon === '<i class="fa fa-thumbs-o-up" style="font-size:24px"></i>') {
        var action = "Add";
    }
    fetch(`/post/${username}/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            liked_action: action
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
    });
    console.log(likes);
    if (action==="Add") {
        var likes = document.querySelector(`#likes-count-${post_id}`).innerHTML;
        document.querySelector(`#like-button-${post_id}`).innerHTML = `<i class="fa fa-thumbs-up" style="font-size:24px; color: blue;"></i>`;
        likes++;
        document.querySelector(`#likes-count-${post_id}`).innerHTML = likes;
    }
    else {
        var likes = document.querySelector(`#likes-count-${post_id}`).innerHTML;
        document.querySelector(`#like-button-${post_id}`).innerHTML = `<i class="fa fa-thumbs-o-up" style="font-size:24px"></i>`;
        likes--;
        document.querySelector(`#likes-count-${post_id}`).innerHTML = likes;
    }
}