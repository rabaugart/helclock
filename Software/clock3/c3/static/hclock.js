const socket = new WebSocket(`ws://${document.location.hostname}:8765`);

function colchanged(event) {
  let t = event.target;
  console.info("Changed ", t.id, t.valueAsNumber);
  socket.send(`Changed ${t.id} ${t.valueAsNumber}`);
}

socket.addEventListener("message", (event) => {
  set_status_message(`Message from server ${event.data}`);
});

function set_status_message(status_msg) {
  let m = document.getElementById("status_message");
  m.innerHTML = status_msg;
}

function ondocload(event) {
  console.log("Starting hclock");
  let csls = document.getElementsByClassName("colslider");
  for (let i = 0; i < csls.length; i++) {
    {
      console.log("Found ", csls[i].id);
      csls[i].onchange = colchanged;
    }
  }
}

document.onreadystatechange = ondocload;
