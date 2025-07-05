document.addEventListener("DOMContentLoaded",function(){
    const container = document.querySelector('.django-messages');
    if (container){
        setTimeout(() => {
            container.querySelectorAll('.django-alert').forEach((element) => {
                element.classList.add("opacity-0");
                setTimeout(()=> element.remove(),500)
            });
        }, 3000)
    }
});