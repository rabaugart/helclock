const socket = new WebSocket(
  `ws://${document.location.hostname}:${ws_server_port}`,
);

function col_slider_changed(event) {
  let t = event.target;
  console.info("Changed ", t.id, t.valueAsNumber);
  socket.send(`Changed ${t.id} ${t.valueAsNumber}`);
}

function col_button_changed(event) {
  let t = event.target;
  console.info("Changed ", t.id, t.id);
  socket.send(`Changed ${t.id}`);
}

socket.addEventListener("message", (event) => {
  set_status_message(`Message from server ${event.data}`);
});

function set_status_message(status_msg) {
  let m = document.getElementById("status_message");
  m.innerHTML = status_msg;
}

function set_color_slider_value(id, value) {
  let m = document.getElementById(id);
  m.value = value;
}

function ondocload(event) {
  console.log("Starting hclock");
  let csls = document.getElementsByClassName("colslider");
  for (let i = 0; i < csls.length; i++) {
    {
      console.log("Found ", csls[i].id);
      csls[i].onchange = col_slider_changed;
    }
  }
  let cbus = document.getElementsByClassName("colbutton");
  for (let i = 0; i < cbus.length; i++) {
    {
      console.log("Found button", cbus[i].id);
      cbus[i].onclick = col_button_changed;
    }
  }
}

document.onreadystatechange = ondocload;
