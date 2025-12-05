import Message from "./pages/Message";
import Counter from "./pages/Counter";
import FormPractice from "./pages/FormPractice";

function App() {
  return (
    <div>
      <h2>Task 2 — Components, Props, useState, useEffect</h2>

      <h3>Props Example</h3>
      <Message text="Hello, I came from props!" />
      <Message text="Props make components reusable." />
      <hr />
      <Counter />
      <hr />
      <FormPractice />
    </div>
  );
}

export default App;
