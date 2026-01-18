document.addEventListener('DOMContentLoaded', () => {
    initCheckToken()
    initLoadComments()
    initScrollForPosts(); // 1
    initLoginCont();
    initThemeSelector(); // 1
    initScroll();
    initSettingsPasswordWrapper();
    initThemeFollows();
    initImageUploader(); // 1
    initHiddenNotifications();
    initLoadCommentForm();
    initLoadProfileData();
    initLoadPostComments();
    initPostLikes();
    initPostBookmarks(); // 1
    initCommentLikes(); // 1
    initCommentBookmarks(); // 1
    initCommentLikes(); // 1 except profile
    initUserFollows();

    if (nextPostsPageUrl && path.endsWith('/')) {
        initLoadPosts();
    }

    if (path.startsWith('/post/')) {
        async function wait() {
            nextCommentsPageUrl = `${BASE_URL}/frontend-api/v1/comments/?post-pk=${postID}`
            isLoadingComments = false;
            isLoadingPosts = true;
            localStorage.setItem('isSearchMode', 'false')
            localStorage.setItem('moreComments', false)
            await initLoadPostComments();
        }
        wait()

    }

})