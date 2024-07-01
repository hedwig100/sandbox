import './App.css';
import { useState } from 'react';

function MyButton() {
  const [count, setCount] = useState(0);

  const handleClick = () => {
    setCount(count + 1);
  }

  return (
    <button onClick={handleClick}>
      Clicked {count} times
    </button>
  );
}

function MyButton2({count, onClick}) {
  return (
    <button onClick={onClick}>
    Clicked {count} times
    </button>
  );
}

export default function App() {
  const [count, setCount] = useState(0);
  const handleClick = () => {
    setCount(count + 1);
  }

  return (
    <div>
      <h1>Counters that update separately</h1>
      <MyButton />
      <MyButton />
      <h1>Counters that update toghther</h1>
      <MyButton2 count={count} onClick={handleClick} />
      <MyButton2 count={count} onClick={handleClick} />
    </div>
  )
}
