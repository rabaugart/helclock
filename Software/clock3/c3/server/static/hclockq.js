const ws = new WebSocket(`ws://${location.host}/ws`);

class Controler {
  policies = ["A", "B", "C"];
  selpol = null;

  button_callback(pol) {
    console.log("Button callback", pol);
    if (ws.readyState == WebSocket.OPEN) {
      const m = {};
      m[MK_mtype] = MT_GENERATOR_SELECT;
      m[MK_selected_generator] = pol;

      console.log(`Sending ${m}`);
      ws.send(JSON.stringify(m));
    }
    for (const pi of this.policies) {
      const bi = document.getElementById(`polbu-${pi}`);
      bi.className = pi == pol ? "sel" : "";
    }
    this.selpol = pol;
  }

  appendButtons() {
    const bf = document.getElementById("button_frame");
    for (const bi of this.policies) {
      let bu = document.createElement("button");
      bu.innerText = bi;
      bu.id = `polbu-${bi}`;
      bu.onclick = (e) => this.button_callback(bi);
      bf.appendChild(bu);
    }
    this.button_callback(this.policies[0]);
  }
}

const con = new Controler();

ws.addEventListener("message", function (event) {
  const obj = JSON.parse(event.data);
  const mt = obj[MK_mtype];
  if (mt == MT_STATUS) {
    document.getElementById("status").innerText = "Status erhalten";
  } else {
    console.log("Got", event.data);
  }
});

function send_startup(e) {
  const m = {};
  m[MK_mtype] = MT_STARTUP;
  ws.send(JSON.stringify(m));
}

ws.onopen = send_startup;

function col_slider_changed(sect, col, value) {
  console.log("Ändere", sect, col, value, con.selpol);
}

function ondocload(event) {
  console.log("Starting hclock");
  con.appendButtons();
  const dsl = document.getElementById("slider");
  const sect = ["Vordergrund", "Hintergrund"];
  const cols = ["rot", "grün", "blau"];
  for (const si of sect) {
    let di = document.createElement("div");
    di.className = "sectdiv";
    let ssi = document.createElement("span");
    ssi.className = "sectspan";
    ssi.appendChild(document.createTextNode(si));
    di.appendChild(ssi);
    for (const ci of cols) {
      let sp = document.createElement("span");
      //sp.appendChild(document.createTextNode(ci));
      let bu = document.createElement("input");
      bu.id = ci;
      bu.type = "range";
      bu.min = 0;
      bu.max = 255;
      bu.onchange = (e) => col_slider_changed(e.target.valueAsNumber, si, ci);
      sp.appendChild(bu);
      sp.className = `farb-slider ${ci}-slider`;
      di.appendChild(sp);
    }
    dsl.appendChild(di);
  }
}

document.onreadystatechange = ondocload;
