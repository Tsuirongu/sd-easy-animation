import React from 'react';
import logo from './logo.svg';
import './App.css';
import Timeline from './component/timeline-editor';

var layers = [
  {
    id: "3d1df1b4-4d9d-45a4-bf14-cb580ee74675",
    name: "RawFrames"
  },
  {
    id: "7d8c4210-0cfa-4a10-8b21-01e6601e00bf",
    name: "ControlNet"
  },
  {
    id: "65079f30-47a8-4469-833e-4f0eea04d233",
    name: "Tile"
  }
];
var frames = {
  "3d1df1b4-4d9d-45a4-bf14-cb580ee74675": [
    {
      name: "Hello.png",
      second: 0,
      duration: 70
    },
    {
      name: "Welcome.png",
      second: 130,
      duration: 200
    }
  ],
  "7d8c4210-0cfa-4a10-8b21-01e6601e00bf": [
    {
      name: "Goodbye.png",
      second: 10,
      duration: 150
    }
  ],
  "65079f30-47a8-4469-833e-4f0eea04d233": []
};

function onUpdateFrames(frames: any) {
  //TODO: deal with frames
  console.log(frames);
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          IFrame Test.
        </p>
        <div>
        <Timeline
          layers={layers}
          frames={frames}
          onUpdateFrames={onUpdateFrames}
        />
        </div>
      </header>
    </div>
  );
}

export default App;
