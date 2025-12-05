import { useState, useEffect } from "react";

export default function Counter() {

  const [count, setCount] = useState(0);

  useEffect(() => {
    console.log("Counter component loaded");
  }, []);

  return (
    <div>
      <h3>Counter Example</h3>
      <p>Count: {count}</p>

      <button onClick={() => setCount(count + 1)}>
        Increase
      </button>
    </div>
  );
}
