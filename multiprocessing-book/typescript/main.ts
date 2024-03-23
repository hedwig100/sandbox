
async function getData(url: string): Promise<any> {
  const response = await fetch(url);
  return response.json();
}

function timer(sec: number): Promise<number> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(sec);
    }, sec*1000);
  })
}

const data = getData('https://jsonplaceholder.typicode.com/posts/1');
const time = timer(2);
console.log('Fetching data and waiting for 2 seconds...');
console.log(await time);
console.log(await data);
