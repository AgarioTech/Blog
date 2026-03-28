window.isLoadingPosts = false;
window.isLoadingComments = true;
window.postsContainer = document.querySelector('.post-container');
window.profileContentContainer = document.querySelector('.profile__content-container');
window.commentsContainer = document.querySelector('.comments-list');
window.postDetailContainer = document.querySelector('.post');
window.lastQuery = '';
window.selectedFile = null;
window.postFilter = null;
window.postType = null;
window.nextPostsPageUrl = null;
window.nextCommentsPageUrl = null;
window.path = window.location.pathname;
window.moreCommentsButton = null

//if (!postsContainer.innerHTML.trim()) {
//    postsContainer.style.display = 'none'
//}