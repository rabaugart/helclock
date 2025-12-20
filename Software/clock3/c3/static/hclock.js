const socket = new WebSocket(`ws://${document.location.hostname}:8765`);

function colchanged(event) {
  let t = event.target;
  console.info("Changed ", t.id, t.valueAsNumber);
  socket.send(`Changed ${t.id} ${t.valueAsNumber}`);
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
