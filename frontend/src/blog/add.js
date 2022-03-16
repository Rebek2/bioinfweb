import { useState } from "react";
import React from 'react';
import { useHistory } from "react-router-dom";

const Create = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [author, setAuthor] = useState('mario');
  const[isPending,setIsPending] = useState(false);
  const history = useHistory();

  const handleSubmit = (e) => {
    e.preventDefault();
    const blog = { title, content, author };
    setIsPending(true)
    fetch('http://127.0.0.1:8000/api/posts/', {
      method: 'POST',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(blog)
    }).then(() => {
      // history.go(-1);
      history.push('/blog');
    })
  }
  return (
    <div className="container">

      <form onSubmit={handleSubmit}>
        <div class = 'mb-3'>
        <label for= "exampleFormControlInput1" class="form-label">Blog title:</label>
        <input 
          type="text" 
          class='form-label'
          placeholder="Tytuł.."
          required 
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        </div>
        <div class ='mb-3'>
        <label>Blog content:</label>
        <textarea
          required
          value={content}
          onChange={(e) => setContent(e.target.value)}
        ></textarea>
        </div>
        <div class ='mb-3'>
        <label>Blog author:</label>
        <select
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
        >
          <option value="mario">mario</option>
          <option value="yoshi">yoshi</option>
        </select>
        </div>
        {!isPending && <button type = 'submit' class = 'btn btn-primary'>Add Blog</button>}
        { isPending && <button disabled type = 'submit' class = 'btn btn-primary'>Adding Blog</button>}

      </form>
    </div>
  );
}

function App3() {
  return (
    <div class ='container'>
      <h2>Dodaj nowy post:</h2>
      <Create/>
    
    </div>
  )
}

export default App3;