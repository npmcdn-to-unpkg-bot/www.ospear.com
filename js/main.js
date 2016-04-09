$(function() {
  // メニュークリックでスクロール
  $('#menu a[href^="#"]').click(function() {
    var speed = 500;
    var $target = $($(this).attr("href"));
    var position = $target.offset().top;
    $("html, body").animate({scrollTop:position}, speed, "swing");
    return false;
  });

  // フッターのリンククリックでモーダル表示
  var onModal = false;
  $('footer a').click(function() {
    var href = $(this).attr('href');
    var $target = $(href);
    if (onModal) {
      $(onModal).fadeOut()
    }
    $target.fadeIn(function() {
      onModal = href;
    });
  });
  // モーダル外クリックで閉じる
  $(document).click(function(event) {
    if (onModal && !$.contains($(onModal)[0], event.target)) {
      $(onModal).fadeOut(function() {
        onModal = false;
      });
    }
  });
  // ESCでモーダル閉じる
  $(document).keyup(function(e) {
    if (onModal && e.keyCode == 27) {
      $(onModal).fadeOut(function() {
        onModal = false;
      });
    }
  });

  var validate = function(req) {
    return true;
  };
  // Products
  var $products = $('#products ul').masonry({
    itemSelector: 'li',
    columnWidth: 'li',
    percentPosition: true
  })
  $products.imagesLoaded().progress(function() {
    $products.masonry('layout');
  });
  // Contact
  $('#contactForm').submit(function() {
    $this = $(this);
    var submit = $this.find('input[name="submit"]')
                   .attr('disabled', true)
                   .val('送信中...');
    var req = {
      office:  $this.find('input[name="office"]').val(),
      name:    $this.find('input[name="name"]').val(),
      address: $this.find('input[name="address"]').val(),
      tel:     $this.find('input[name="tel"]').val(),
      email:   $this.find('input[name="email"]').val(),
      content: $this.find('textarea[name="content"]').val()
    };
    if (!validate(req)) {
      alert('入力に不備があります。');
      return;
    }
    if (!confirm('送信してよろしいですか？')) {
      return;
    }
    var msg = $this.find('.msg').hide().removeClass('done fail');
    $.ajax({
      type: "POST",
      url: "/contact",
      data: req
    }).done(function(res) {
      if (res.success) {
        msg.addClass('done')
          .text('')
          .append(document.createTextNode(req.office + ' ' + req.name))
          .append('様<br/>お問い合わせありがとうございました。<br />ご回答まで今しばらくお待ちください。')
          .show();
      } else if (res.errors.system_error) {
        msg.addClass('fail')
          .text('サーバエラーのため、お問い合わせ送信が失敗しました。時間を置いて再度お問い合わせ送信をお願い致します。')
          .show();
      } else {
        msg.addClass('fail')
          .text('入力に誤りがあったため、お問い合わせ送信を中断しました。')
          .show();
      }
    }).fail(function(res) {
      msg.addClass('fail')
        .text('正常に送信できませんでした。再度のお問い合わせ送信をお願い致します。')
        .show();
    }).always(function() {
      submit.attr('disabled', false).val('お問い合わせ');
    });
    return false;
  });
});

