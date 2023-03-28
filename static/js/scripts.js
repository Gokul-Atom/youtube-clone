const player = document.querySelector("iframe.player");
const sidebar = document.querySelector(".sidebar");
const playlist = document.querySelectorAll(".video-list .video-group > img");
const topTags = document.querySelector("div.tags");
const description = document.querySelector(".description p")
const tags = document.querySelector(".selected-tags");
const videoTags = document.querySelector("#video-tags");
const videopage = document.querySelector(".player-grid-layout");
const notificationsModal = document.querySelector("#notificationsModal")
const channelPage = document.querySelector("#videos.tab-pane");
const registerForm = document.querySelector(".login-register > .register");
const loginForm = document.querySelector(".login-register > .login");
const uploadCoverField = document.querySelector("#id_cover_photo");
const uploadLogoField = document.querySelector("#id_logo");
const uploadAvatarField = document.querySelector("#file");
const videoUploadForm = document.querySelector(".video-upload");
const uploadThumbnailField = document.querySelector("#id_thumbnail");
const navbarSearchbar = document.querySelector("#navbar-search");
const confirmBtn = document.querySelector("#modal > div > div > div.modal-footer > form");
const modalBtn = document.querySelector("#modal-btn");
const editCommentBtn = document.querySelector("#edit-comment-btn");
const modalContent = document.querySelector("#modal-content span");
const commentContent = document.querySelector("#id_edit_comment");
const createChannelForm = document.querySelector("div.create-channel");
const updateChannelForm = document.querySelector("div.update-channel");
const passwordResetForm = document.querySelector("div.password-reset");
// let tagsList = [];

$(document).ready(function() {
    $(".multiple-selection").select2({
        tags: true,
    }
    );
});

function previewImage() {
    console.log(this);
    const files = this.files[0];
    const imgDiv = this.parentElement.querySelector("img");
    if (files) {
        const fileReader = new FileReader();
        fileReader.readAsDataURL(files);
        fileReader.addEventListener("load", function () {
            imgDiv.src = this.result;
        });    
    }
}

function makeBootstrapForm(form) {
    const fields = form.querySelectorAll("form input");
    const textArea = form.querySelectorAll("form textarea");

    fields.forEach((e) => {
        if (e.type == 'checkbox') {
            e.style.margin = "10px 15px";
            e.style.transform = "scale(1.5)";
        } else if (e.type == 'submit') {
            return null;
        } else {
            e.classList.add("form-control");
        }
    });

    textArea.forEach((e) => {
        e.classList.add("form-control");
    });
}

function uploadThumbnail() {
    uploadThumbnailField.click();
}

function confirmDeletion(e) {
    const deleteBtn = document.querySelector("#modal > div > div > div.modal-footer > a.btn.btn-danger")
    let url = e.attributes["data-url"].value;
    modalContent.textContent = e.attributes["data-value"].value;

    if (url.includes("delete-comment")) {
        deleteBtn.setAttribute("data-url", url);
        deleteBtn.setAttribute("onclick", "deleteComment(this)");
    } else {
        deleteBtn.setAttribute("href", url);
    }
}

function editComment(e) {
    const val = e.parentElement.parentElement.querySelector("div > p").textContent;
    const url = e.attributes['data-url'].value;
    commentContent.value = val;
    commentContent.parentElement.action = url;

    setTimeout(function() {
        commentContent.focus();
    }, 900);
}

function deleteFields(e) {
    e.forEach((e1) => e1.remove());
}

// navbar
function revealSearchbar() {
    let searchIcon = document.querySelector("#navbarSupportedContent > ul > li:nth-child(1) > a > svg");
    let secondEl = document.querySelector("#navbarSupportedContent > ul > li:nth-child(2) > a > svg");
    
    if (secondEl) {
        document.querySelector("#navbarSupportedContent > ul > li:nth-child(2) > a > svg").style.cssText = "all 1s ease";
    }
    
    if (navbarSearchbar.classList.contains("reveal-searchbar")) {
        navbarSearchbar.classList.remove("reveal-searchbar");
        searchIcon.innerHTML = `
            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
        `
        if (secondEl) {
            document.querySelector("#navbarSupportedContent > ul > li:nth-child(2) > a > svg").style.width = "16px";
            document.querySelector("#navbarSupportedContent > ul > li:nth-child(2) > a > svg").parentElement.style.padding = "8px";
        }
    } else {
        navbarSearchbar.classList.add("reveal-searchbar");
        searchIcon.innerHTML = `
            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
            <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
            `;
        if (secondEl) {
            document.querySelector("#navbarSupportedContent > ul > li:nth-child(2) > a > svg").style.width = "0px";
            document.querySelector("#navbarSupportedContent > ul > li:nth-child(2) > a > svg").parentElement.style.padding = "0px";
        }

        setTimeout(function() {
            document.querySelector("#navbar-search > input").focus();
            console.log("clicked");
        }, 100);
    }
}

// notifications
function toggleNotifications() {
    document.querySelector("#notifications-btn").click();
    if (notificationsModal.classList.contains('show')) {
        notificationsModal.classList.remove('show');
    } else {
        notificationsModal.classList.add('show');
    }
    console.log("OK");
}

// player-size
function playerSizeAdjust() {
    if (player) {
        let playerHeight = player.clientWidth * 9 / 16;
        player.style.height = `${playerHeight}px`;
    }

    if (playlist && videopage) {
        playlist.forEach((e) => {
            e.style.height = `${e.clientWidth * 9 / 16}px`;
        });
        let tagWidth = playlist[0].clientWidth + 34;
        // console.log(playlist[0].clientWidth);
        // console.log(tagWidth);
        topTags.style.width = (tagWidth) + "px";
    }
}

// description
function toggleContentVisibility() {
    if (description && document.querySelector(".description a")) {
        if (description.classList.contains("show-content")) {
            description.classList.remove("show-content");
            document.querySelector(".description a").textContent = "Show more";
            window.scrollTo(0, 0);
        } else {
            description.classList.add("show-content");
            document.querySelector(".description a").textContent = "Show less";
        }
    }
}

function checkContentHeight() {
    if (description) {
        const height = description.clientHeight;
        const fullHeight = description.scrollHeight;

        if (fullHeight <= height) {
            description.parentElement.children[1].remove();
            description.classList.add("show-content")
        }
    }
}

// related content
function checkPosition() {
    if (player) {
        const playerPos = player.getBoundingClientRect().bottom;
        const relatedContent = document.querySelector("div#related-content h5").getBoundingClientRect().bottom;
        const firstEl = document.querySelector("body > div.d-flex.flex-column.player-layout > div.m-2 > ul > div:nth-child(1)");

        if (playerPos >= relatedContent && window.innerWidth <= 700) {
            topTags.classList.add("fixed-top");
            topTags.style.marginTop = (playerPos - 1) + "px";

            if (firstEl) {
                firstEl.paddingTop = "26px";
                firstEl.classList.add("mt-5");
            }

        } else {
            topTags.classList.remove("fixed-top");
            topTags.style.marginTop = "unset";

            if (firstEl) {
                firstEl.paddingTop = "unset";
                firstEl.classList.remove("mt-5");
            }
        }
    }
}

// sidebar
function toggleSidebar() {
    // if (videoSidebar) {
    //     if (videoSidebar.classList.contains('show')) {
    //         videoSidebar.classList.remove('show');
    //     }
    // }

    if (sidebar) {
        if (sidebar.classList.contains('show')) {
            sidebar.classList.remove('show');
        } else {
            sidebar.classList.add('show');
        }
    }
}

// error message
function hideMessage(e) {
    const elem = e.parentElement.style
    const windowWidth = window.innerWidth;

    elem.transform = 'translateX(-' + windowWidth + 'px)';
    setTimeout(function () {
        elem.position = 'absolute';
        elem.visibility = 'hidden';
    }, 500)
}

// video upload
// function addTag() {
//     let tag = document.querySelector(".video-upload .flex input");
//     if (!tagsList.includes(tag.value)) {
//         tagsList.push(tag.value);
//         tags.innerHTML += `
//         <div>
//             <span>${tag.value}</span>
//             <a role="button" onclick="removeTag(this)">
//                 <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
//                     <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
//                 </svg>
//             </a>
//         </div>
//         `;
//     }

//     tag.value = "";
//     updateTags();
// }

// function removeTag(e) {
//     e.parentElement.remove();
//     let index = tagsList.indexOf(e.parentElement.children[0].textContent);
//     tagsList.splice(index, 1);
//     updateTags();
// }

// function updateTags() {
//     videoTags.value = "";
//     tagsList.forEach((e) => {
//         videoTags.value += e + ";";
//     });
// }

function addClassVideoUploadForm() {
    if (videoUploadForm) {
        makeBootstrapForm(videoUploadForm);
    }
}

function uploadThumbnail() {
    uploadThumbnailField.click();
}

// edit video

// register form
function addClassRegisterForm() {
    if (registerForm) {
        makeBootstrapForm(registerForm);
    }
}

// channel page
function stickyTop(){
    if (channelPage) {
        const tab = document.querySelector("body > div.channel-div > div.d-flex.text-light");
        const tabContent = document.querySelector("body > div.channel-div > div.tab-content");
        if (document.querySelector("body > div.channel-div > hr").getBoundingClientRect().bottom < 50) {
            tab.style.paddingTop = "50px";
            tab.classList.replace("sticky-top", "fixed-top");
            tab.style.borderBottom = "1px solid white";
            tabContent.style.marginTop = "50px";
        } else {
            tab.style.paddingTop = "0px";
            tab.classList.replace("fixed-top", "sticky-top");
            tab.style.borderBottom = "none";
            tabContent.style.marginTop = "unset";
        }
    }
}

// update channel
function uploadCoverPhoto() {
    uploadCoverField.click();
}

function uploadChannelLogo() {
    uploadLogoField.click();
}

// update profile
function uploadAvatar() {
    uploadAvatarField.click();
}

// form validation
function validateForm(event) {
    console.log("valid")
    event.preventDefault();
    const form = $(this);
    const errorFields = document.querySelectorAll(".text-danger.ps-0 li");

    deleteFields(errorFields);

    $.ajax({
        type: "POST",
        url: form.attr('action'),
        data: form.serialize(),
        success: function(data) {
            console.log(data);
            if (!data.includes("[")) {
                location.replace(data);
            } else {
                const result = JSON.parse(data);
                console.log(result);
                const keys = Object.keys(result);
                console.log(keys);
                keys.forEach((e1) => {
                    result[e1].forEach((e2) => {
                        if (e2 == "“” is not a valid value.") {
                            $(`#required-${e1}`).append(`<li class="list-unstyled">Please select minimum one tag.</li>`);
                        } else {
                            $(`#required-${e1}`).append(`<li class="list-unstyled">${e2}</li>`);
                        }
                    });
                });
            }
        }
    });
}

// register
function validatePassword() {
    const password1 = document.querySelector("#id_password1");
    const password2 = document.querySelector("#id_password2");
    if (password1.value != password2.value) {
        document.querySelector("#required-password2").innerHTML = '<li class="list-unstyled">Password don\'t match.</li>';
    } else {
        document.querySelector("#required-password2").innerHTML = '';
    }
}

// login
function valiadateLoginForm(event) {
    event.preventDefault();
    this.submit();
}

// AJAX
function checkHandle() {
    $("#required-handle").html("");
    $.ajax({
        type: "POST",
        url: checkHandleUrl,
        headers: {"X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()},
        data: {
            handle: $("#id_handle").val(),
        },
        success: function(data) {
            if (data == "true") {
                $("#required-handle").html("<p class='text-danger'>Handle already taken.<p>");
            } else {
                $("#required-handle").html("<p class='text-success'>Handle available.<p>");
            }
        }
    });
}

function checkUsername() {
    $("#required-username").html("");
    $.ajax({
        type: "POST",
        url: checkUsernameUrl,
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: {
            username: $("#id_username").val(),
        },
        success: function(data) {
            if (data == "true") {
                $("#required-username").html("<p class='text-danger'>Username already taken.</p>");
            } else {
                $("#required-username").html("<p class='text-success'>Username available.</p>");
            }
        }
    });
}

// password reset
function checkEmail(event) {
    $("#required-username").html("");

    $.ajax({
        type: "GET",
        url: "",
        data: $(".password-reset form").serialize(),
        success: function(data) {
            console.log(data);
            if (data == "true") {
                $("#required-email").html(`<p class='text-success'>User account exists. OTP will be sent shortly to <u>${$("#id_email").val()}</u> once <b>Reset Password</b> button is clicked.</p>`);
                // $("#id_email").attr('disabled', '');
                $(".password-reset form button").removeAttr('disabled');
            } else {
                $("#required-email").html("<p class='text-danger'>User account doesn't exists.</p>");
            }
        }
    });
}

function generateResetLink(event) {
    event.preventDefault();
    $("#required-email").html("");
    $("#id_reset_form").removeAttr("hidden");

    const errorFields = document.querySelectorAll(".text-danger.ps-0 li");
    console.log(errorFields);
    deleteFields(errorFields);

    $.ajax({
        type: "POST",
        url: resetPasswordUrl,
        data: $(".password-reset form").serialize(),
        success: function(data) {
            console.log(data);
            if (!data.includes("[")) {
                location.replace(data);
            } else {
                const result = JSON.parse(data);
                console.log(result);
                const keys = Object.keys(result);
                console.log(keys);
                keys.forEach((e1) => {
                    result[e1].forEach((e2) => {
                        if (e2 != "OTP incorrect!" && e2 != "OTP cannot be empty." && e2 != "OTP expired!") {
                            $(`#required-otp`).html(`<li class="list-unstyled text-success">OTP verified!</li>`);
                            // $("#id_otp").attr("disabled", "");
                            $(".password1").removeAttr("hidden");
                            $(".password2").removeAttr("hidden");
                        }
                        $(`#required-${e1}`).append(`<li class="list-unstyled">${e2}</li>`);
                    });
                });
            }
        }
    });
}

function updateCommentContent(data) {
    $("#id_comments_div").html(data);
    commentCount();
}

function commentCount() {
    setTimeout(function() {
        $("#comment-count").text(`${$("#id_comments").attr('data-count')} Comments`);
    }, 300);
}

function addComment(event) {
    event.preventDefault();

    form = $(this);
    $.ajax({
        type: "POST",
        url: form.attr("href"),
        data: form.serialize(),
        success: updateCommentContent,
    });
    this.reset();
    this.children[1].blur();
}

function updateComment(event) {
    event.preventDefault();
    const form = $(this);

    $.ajax({
        type: "POST",
        url: form.attr("action"),
        data: form.serialize(),
        success: updateCommentContent,
    });
    $("#comment-modal").modal("hide");
}

function deleteComment(e) {
    $.ajax({
        type: "DELETE",
        url: e.attributes["data-url"].value,
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').prop('value')},
        data: {},
        success: updateCommentContent,
    });
    $("#modal").modal("hide");
}

function subscribeChannel(event) {

    $.ajax({
        type: "POST",
        url: $(event).attr("data-url"),
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').prop('value')},
        data: {},
        success: function(data) {
            $("#subs-btn").text("Unsubscribe");
            $("#subs-count").text(data);
        }
    });
    const dataUrl = $("#subs-btn").attr("data-url").replace("subscribe", "unsubscribe");
    $("#subs-btn").attr("data-url", dataUrl);
    $("#subs-btn").attr("onclick", "unsubscribeChannel(this)");
}

function unsubscribeChannel(event) {

    $.ajax({
        type: "POST",
        url: $(event).attr("data-url"),
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').prop('value')},
        data: {},
        success: function(data) {
            $("#subs-btn").text("Subscribe");
            $("#subs-count").text(data);
        }
    });
    const dataUrl = $("#subs-btn").attr("data-url").replace("unsubscribe", "subscribe");
    $("#subs-btn").attr("data-url", dataUrl);
    $("#subs-btn").attr("onclick", "subscribeChannel(this)");
}

function likeVideo(event) {
    $.ajax({
        type: "POST",
        url: $(event).attr("data-url"),
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').prop('value')},
        data: {},
        success: function(d) {
            const data = JSON.parse(d);
            $("#likes").text(data["likes"]);
            $("#dislikes").text(data["dislikes"]);
            $("#dislikes").parent().css("background-color", "revert");
            $("#likes").parent().css("background-color", "green");
        }
    });
}

function dislikeVideo(event) {
    $.ajax({
        type: "POST",
        url: $(event).attr("data-url"),
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').prop('value')},
        data: {},
        success: function(d) {
            const data = JSON.parse(d);
            $("#likes").text(data["likes"]);
            $("#dislikes").text(data["dislikes"]);
            $("#likes").parent().css("background-color", "revert");
            $("#dislikes").parent().css("background-color", "red");
        }
    });
}

$(".comment-form form").on("submit", addComment);
$("#comment-form").on("submit", updateComment);

// EVENT LISTENERS
if (player) {
    window.addEventListener('resize', playerSizeAdjust);
    window.addEventListener('scroll', checkPosition);
}

window.addEventListener('scroll', stickyTop);
// notificationBtn.addEventListener('click', toggleNotifications);
if (uploadCoverField)
    uploadCoverField.addEventListener('change', previewImage);

if (uploadLogoField)
    uploadLogoField.addEventListener('change', previewImage);

if (uploadAvatarField)
    uploadAvatarField.addEventListener('change', previewImage);

if (uploadThumbnailField) {
    uploadThumbnailField.addEventListener('change', previewImage);
}

if (registerForm) {
    let timer = null;
    registerForm.querySelector("form").addEventListener("submit", validateForm);
    document.querySelector("#id_username").addEventListener("input", function() {
        clearTimeout(timer);
        timer = setTimeout(checkUsername, 2000);
    });
    document.querySelector("#id_password1").addEventListener("input", validatePassword);
    document.querySelector("#id_password2").addEventListener("input", validatePassword);
}

if (loginForm) {
    loginForm.querySelector("form").addEventListener("submit", valiadateLoginForm);
}

if (createChannelForm) {
    let timer = null;
    createChannelForm.querySelector("form").addEventListener("submit", validateForm);
    document.querySelector("#id_handle").addEventListener("input", function() {
        clearTimeout(timer);
        timer = setTimeout(checkHandle, 2000);
    });
}

if (updateChannelForm) {
    updateChannelForm.querySelector("form").addEventListener("submit", validateForm);
}

if (videoUploadForm) {
    videoUploadForm.querySelector("form").addEventListener("submit", validateForm);
}

if (passwordResetForm) {
    let timer = null;
    passwordResetForm.querySelector("form").addEventListener("submit", generateResetLink);
    document.querySelector("#id_email").addEventListener("input", function() {
        clearTimeout(timer);
        timer = setTimeout(checkEmail, 2000);
    });
}

document.onload = playerSizeAdjust();
document.onload = checkContentHeight();
document.onload = addClassRegisterForm();
document.onload = addClassVideoUploadForm();
document.onload = commentCount();
