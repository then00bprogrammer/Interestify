export const toggleBookmark = async (
    isBookMarked: boolean,
    ArticleId: string,
    currentUser: any,
    ) => {
    const email = currentUser.email;
    if (!isBookMarked) {
        await fetch(`https://nikhilranjan.pythonanywhere.com/addBookmark?email=${email}&id=${ArticleId}`);
        console.log("SUCCESSFULLY ADDED");
    } else {
        await fetch(`https://nikhilranjan.pythonanywhere.com/deleteBookmark?email=${email}&id=${ArticleId}`);
        console.log("DELETED SUCCESSFULLY");
    }
};
