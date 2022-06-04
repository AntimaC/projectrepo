const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a')

allSideMenu.forEach((item) => {
  const li = item.parentElement

  item.addEventListener('click', function () {
    allSideMenu.forEach((i) => {
      i.parentElement.classList.remove('active')
    })
    li.classList.add('active')
  })
})

// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu')
const sidebar = document.getElementById('sidebar')

menuBar.addEventListener('click', function () {
  sidebar.classList.toggle('hide')
})

// const searchButton = document.querySelector('#content nav form .form-input button');
// const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
// const searchForm = document.querySelector('#content nav form');

// searchButton.addEventListener('click', function (e) {
//   if (window.innerWidth < 576) {
//     e.preventDefault()
//     searchForm.classList.toggle('show')
//     if (searchForm.classList.contains('show')) {
//       searchButtonIcon.classList.replace('bx-search', 'bx-x')
//     } else {
//       searchButtonIcon.classList.replace('bx-x', 'bx-search')
//     }
//   }
// })

// if (window.innerWidth < 768) {
//   sidebar.classList.add('hide')
// } else if (window.innerWidth > 576) {
//   searchButtonIcon.classList.replace('bx-x', 'bx-search')
//   searchForm.classList.remove('show')
// }

window.addEventListener('resize', function () {
  if (this.innerWidth > 576) {
    searchButtonIcon.classList.replace('bx-x', 'bx-search')
    searchForm.classList.remove('show')
  }
})

// const switchMode = document.getElementById('switch-mode')

// switchMode.addEventListener('change', function () {
//   if (this.checked) {
//     document.body.classList.add('dark')
//   } else {
//     document.body.classList.remove('dark')
//   }
// })


var marker = CKEDITOR.dom.element.createFromHtml( '<span style="margin:0;padding:0;border:0;clear:both;width:1px;height:0px;font-size:0;display:block;">&nbsp;</span>', doc );





$(document).ready(function(){

    $('#menu').click(function(){
        $(this).toggleClass('fa-times');
        $('.navbar').toggleClass('nav-toggle');
    });

   
    $(window).on('load scroll',function(){

        $('#menu').removeClass('fa-times');
        $('.navbar').removeClass('nav-toggle');

        $('.login-form').removeClass('popup');

        $('section').each(function(){

            let top = $(window).scrollTop();
            let height = $(this).height();
            let id = $(this).attr('id');
            let offset = $(this).offset().top - 200;

            if(top > offset && top < offset + height){
                $('.navbar ul li a').removeClass('active');
                $('.navbar').find(`[href="#${id}"]`).addClass('active');
            }


        });

    });

});