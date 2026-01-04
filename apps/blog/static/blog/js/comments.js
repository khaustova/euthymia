'use strict'; 

// CSRF-token

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

// Создание формы для комментария для гостя и для администратора

function createGuestCommentForm(author, parentID, commentID = -1) {
    const commentFormTemplate = `
    <div class="comment-reply-form">
    <div><span class="comment-close-icon" onclick="closeCommentForm()"><i class="fas fa-times"></i></span></div>
    <form method="post" id="newCommentForm" class="comment-form">
        <select name="parent" id="id_parent">
            <option value="` + parentID + `" selected="` + parentID + `"></option>
        </select>
        <textarea name="body" cols="40" rows="10" class="comment-form__comment-field" placeholder="Оставьте комментарий..." required="" maxlength="800" id="id_body">`
        + author +
        `, </textarea>
        <div class="comment-form-fields">
            <input type="text" name="guest" class="comment-form__name-field custom-input" placeholder="Имя" autocomplete="on" maxlength="250" id="id_guest">
            <input type="email" name="email" class="comment-form__email-field custom-input" placeholder="E-mail" autocomplete="on" maxlength="254" id="id_email">
        <button type="submit">Отправить</button>
        <input type="hidden" name="csrfmiddlewaretoken" value="` + csrftoken + `"></div>
    </form>
    </div>`;
    createForm(author, parentID, commentID, commentFormTemplate);
}

function createAdminCommentForm(author, parentID, commentID = -1) {
    const commentFormTemplate = `
    <div class="comment-reply-form">
    <div><span class="comment-close-icon" onclick="closeCommentForm()"><i class="fas fa-times"></i></span></div>
    <form method="post" id="newCommentForm" class="comment-form">
        <select name="parent" id="id_parent">
            <option value="` + parentID + `" selected="` + parentID + `"></option>
        </select>
        <textarea name="body" cols="40" rows="10" class="comment-form__comment-field" placeholder="Оставьте комментарий..." required="" maxlength="800" id="id_body">`
        + author +
        `, </textarea>
        <div class="comment-form-fields">
            <button type="submit">Отправить</button>
        <input type="hidden" name="csrfmiddlewaretoken" value="` + csrftoken + `"></div>
    </form>
    </div>`;
    createForm(author, parentID, commentID, commentFormTemplate);
}

function createForm(author, parentID, commentID, template) {
    if (document.contains(document.getElementById('newCommentForm'))) {
        document.getElementsByClassName('comment-reply-form')[0].remove();
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

// Удаление формы для комментария

function closeCommentForm () {
    document.getElementsByClassName('comment-reply-form')[0].remove();
}