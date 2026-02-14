function myFunction() {
  clock();
  setInterval("clock();", 1000);
}

function clock() {
  const canvas = document.getElementById("clock");
  const ctx = canvas.getContext("2d");
  const endPoint = {x: canvas.width, y: canvas.height};
  const center = {x: endPoint.x / 2, y: endPoint.y / 2};
  const rad = endPoint.x * 0.8 / 2;

  // 時間取得
  const now = new Date;
  const hh = now.getHours();
  const mm = now.getMinutes();
  const ss = now.getSeconds();

  // ラインの起点を求める
  const getLine = (center, rad, num, den, size) => {
    const x = center.x + (Math.cos(Math.PI * 2 * (num / den) - Math.PI / 2) * rad) * size;
    const y = center.y + (Math.sin(Math.PI * 2 * (num / den) - Math.PI / 2) * rad) * size;
    return [x, y];
  };

  // 描画リセット
  ctx.clearRect(0, 0, endPoint.x, endPoint.y);

  // 時計枠
  ctx.strokeStyle = "black";
  ctx.beginPath();
  ctx.lineWidth = 2;
  ctx.arc(center.x, center.y, rad, 0, Math.PI * 2);
  ctx.stroke();

  // 目盛り
  for (var i = 0; i < 60; i++) {
    let arg = [];
    ctx.beginPath();
    if (i % 5 === 0) {
      ctx.lineWidth = 5;
      arg.push(60 , 0.9);
    } else {
      ctx.lineWidth = 2;
      arg.push(60, 0.95);
    }
    ctx.moveTo(...getLine(center, rad, i, ...arg));
    ctx.lineTo(...getLine(center, rad, i, 60 , 1));
    ctx.stroke();
  }

  // 時針
  ctx.beginPath();
  ctx.lineWidth = 8;
  ctx.moveTo(center.x, center.y);
  const m = 0.2 * Math.floor(mm / 12);
  ctx.lineTo(...getLine(center, rad, hh + m, 12, 0.6));
  ctx.stroke();

  // 分針
  ctx.beginPath();
  ctx.lineWidth = 5;
  ctx.moveTo(center.x, center.y);
  ctx.lineTo(...getLine(center, rad, mm, 60, 0.75));
  ctx.stroke();

  // 秒針
  ctx.beginPath();
  ctx.strokeStyle = "red";
  ctx.lineWidth = 2;
  ctx.moveTo(center.x, center.y);
  ctx.lineTo(...getLine(center, rad, ss, 60, 0.9));
  ctx.stroke();

  // 中心軸
  ctx.beginPath();
  ctx.strokeStyle = "black"
  ctx.fillStyle = "white"
  ctx.arc(center.x, center.y, 7, 0, Math.PI * 2, true);
  ctx.fill();
  ctx.stroke();

  // 時刻文字
  ctx.strokeStyle = "red";
  ctx.fillStyle = "red";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.font = "bold 25px 'MS Gothic', sans-serif";
  ctx.beginPath();
  ctx.fillText( "I.system", ...getLine(center, rad, 0, 60, 0.4));
  ctx.stroke();
  ctx.font = "30px Roboto nedium";
  ctx.strokeStyle = "black"
  ctx.fillStyle = "black";
  var t = 0;
  for (var i = 0; i < 60; i++) {
    ctx.beginPath();
    if (i % 5 === 0) {
        ctx.fillText( t===0 ? "12" : t.toString(), ...getLine(center, rad, i, 60, 0.8));
        t = t + 1;
    }
    ctx.stroke();
  }
  ctx.strokeStyle = "blue"
  ctx.fillStyle = "blue";
  ctx.font = "bold 25px 'MS Gothic', sans-serif";
  ctx.beginPath();
  let stime = hh.toString().padStart( 2,'0') + ":" + mm.toString().padStart( 2,'0') + ":" + ss.toString().padStart( 2,'0');
  ctx.fillText( stime, ...getLine(center, rad, 30, 60, 0.4));
  ctx.stroke();
}
