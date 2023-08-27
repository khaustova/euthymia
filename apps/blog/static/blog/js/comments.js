'use strict'; 

/* CSRF-token */

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + '=') {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue; 
};

const csrftoken = getCookie('csrftoken');

/* Create comment form */

function createGuestCommentForm(author, parentID, commentID = -1) {
    let formClass = '';
    if (commentID != -1) {
        formClass = 'comments__tab';
    } 
    const commentFormTemplate = `
    <div class="comment">
    <p class="comment__info ` + formClass + `"><b>Ответить на комментарий:</b><span class="material-symbols-outlined button-icon" onclick="closeCommentForm()">close</span></p>
    <form method="post" id="newCommentForm" class="comment-form ` + formClass + `">
        <select name="parent" class="comments__parent" id="id_parent">
            <option value="` + parentID + `" selected="` + parentID + `"></option>
        </select>
        <textarea name="body" cols="40" rows="10" class="comment-form__comment-field" placeholder="Оставьте комментарий..." required="" maxlength="800" id="id_body">`
        + author +
        `, </textarea>
        <div class="form-row">
            <span class="material-symbols-outlined input-item">person</span>
            <input type="text" name="guest" class="comment-form__name-field custom-input" placeholder="Имя" maxlength="250" id="id_author">
        </div>
        <div class="form-row">
            <span class="material-symbols-outlined input-item">person</span>
            <input type="email" name="email" class="comment-form__email-field custom-input" placeholder="E-mail" maxlength="254" id="id_email">
        </div>
        <button type="submit" class="comment-form__post-button">Отправить</button> 
        <input type="hidden" name="csrfmiddlewaretoken" value="` + csrftoken + `">
    </form>
    </div>`;
    createForm(author, parentID, commentID, commentFormTemplate);
}

function createAdminCommentForm(author, parentID, commentID = -1) {
    let formClass = '';
    if (commentID != -1) {
        formClass = 'comments__tab';
    } 
    const commentFormTemplate = `
    <div class="comment">
    <p class="comment__info ` + formClass + `"><b>Ответить на комментарий:</b><span class="material-symbols-outlined button-icon" onclick="closeCommentForm()">close</span></p>
    <form method="post" id="newCommentForm" class="comment-form admin-comment-form ` + formClass + `">
        <select name="parent" class="comments__parent" id="id_parent">
            <option value="` + parentID + `" selected="` + parentID + `"></option>
        </select>
        <textarea name="body" cols="40" rows="10" class="comment-form__comment-field" placeholder="Оставьте комментарий..." required="" maxlength="800" id="id_body">`
        + author +
        `, </textarea>
        <button type="submit" class="comment-form__post-button">Отправить</button> 
        <input type="hidden" name="csrfmiddlewaretoken" value="` + csrftoken + `">
    </form>
    </div>`;
    createForm(author, parentID, commentID, commentFormTemplate);
}

function createForm(author, parentID, commentID, template) {
    if (document.contains(document.getElementById('newCommentForm'))) {
        document.getElementsByClassName('comment')[1].remove();
    }
    let parent = document.getElementById(parentID);
    let comment = document.getElementById(commentID);
    const commentFormTemplate = template;
    if (commentID != -1) {
        comment.insertAdjacentHTML('afterEnd', commentFormTemplate);
    }
    else {
        parent.insertAdjacentHTML('afterEnd', commentFormTemplate);
    }
}

/* Remove comment form */

function closeCommentForm () {
    document.getElementsByClassName('comment')[1].remove();
}