$(function(){
  // .js-accordion_titleをクリックすると
  $('.js-accordion_title').click(function(){ 
    // クリックした次の要素を展開
    $(this).next('.js-accordion_inner').slideToggle();
    // 展開するときjs-accordion_titleクラスにopenクラスを追加してアイコンを回転
    $(this).toggleClass("open");
  });
});
