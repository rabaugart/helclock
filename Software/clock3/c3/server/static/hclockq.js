const ws = new WebSocket(`ws://${location.host}/ws`);

class Controler {
  generators = null;
  selpol = null;

  button_callback(pol) {
    const name = pol[MK_generator_name];
    console.log("Button callback", name);
    if (ws.readyState == WebSocket.OPEN) {
      const m = {};
      m[MK_mtype] = MT_GENERATOR_SELECT;
      m[MK_selected_generator] = name;

      console.log(`Sending ${m}`);
      ws.send(JSON.stringify(m));
    }
  }

  set_selected_generator() {
    if (this.selpol) {
      for (const pi of this.generators) {
        const bi = document.getElementById(`polbu-${pi[MK_generator_name]}`);
        if (pi[MK_generator_name] == this.selpol) {
          bi.className = "sel";
          // Setze die Farbsektionen
          const sls = document.getElementById("slider");
          // Lösche vorhandene Sektionen
          while (sls.firstChild) {
            sls.removeChild(sls.firstChild);
          }
          // Iteriere über die neuen Sektionen
          for (const [colseci, coli] of Object.entries(pi[MK_colors])) {
            console.log("Colsec", colseci, coli);
            const div = document.createElement("div");
            const sptext = document.createElement("span");
            sptext.appendChild(document.createTextNode(colseci));
            sptext.className = "farb-slider";
            div.appendChild(sptext);
            div.className = "div-slider";
            for (const ci of ["rot", "grün", "blau"]) {
              let sp = document.createElement("span");
              //sp.appendChild(document.createTextNode(ci));
              let bu = document.createElement("input");
              bu.id = ci;
              bu.type = "range";
              bu.min = 0;
              bu.max = 255;
              bu.value = coli[ci];
              bu.onchange = (e) =>
                col_slider_changed(colseci, ci, e.target.valueAsNumber);
              sp.appendChild(bu);
              sp.className = `farb-slider ${ci}-slider`;
              div.appendChild(sp);
            }
            sls.appendChild(div);
          }
        } else {
          bi.className = "";
        }
      }
    }
  }

  appendButtons() {
    if (this.generators) {
      const bf = document.getElementById("button_frame");
      while (bf.firstChild) {
        bf.removeChild(bf.firstChild);
      }
      for (const gi of this.generators) {
        let bu = document.createElement("button");
        const name = gi[MK_generator_name];
        bu.innerText = name;
        bu.id = `polbu-${name}`;
        bu.onclick = (e) => this.button_callback(gi);
        bf.appendChild(bu);
      }
      if (this.selpol) {
        this.set_selected_generator();
      }
    }
  }

  updateStatus(status_msg) {
    this.generators = status_msg[MK_generators];
    this.selpol = status_msg[MK_selected_generator];
    this.appendButtons();
  }
}

const con = new Controler();

ws.addEventListener("message", function (event) {
  const obj = JSON.parse(event.data);
  const mt = obj[MK_mtype];
  if (mt == MT_STATUS) {
    document.getElementById("status").innerText = "Status erhalten";
    con.updateStatus(obj);
  } else {
    console.log("Got", event.data);
  }
});

function send_startup(e) {
  const m = {};
  m[MK_mtype] = MT_STARTUP;
  ws.send(JSON.stringify(m));
  console.log("Startup sent");
}

ws.onopen = send_startup;

function col_slider_changed(sect, col, value) {
  console.log("Ändere", value, sect, col, con.selpol);
  const d = {};
  d[MK_mtype] = MT_COL_UPDATE;
  d[MK_selected_generator] = con.selpol;
  d[MK_colsec] = sect;
  d[MK_color] = col;
  d[MK_value] = value;
  ws.send(JSON.stringify(d));
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
      bu.onchange = (e) => col_slider_changed(si, ci, e.target.valueAsNumber);
      sp.appendChild(bu);
      sp.className = `farb-slider ${ci}-slider`;
      di.appendChild(sp);
    }
    dsl.appendChild(di);
  }
}

document.onreadystatechange = ondocload;
