import { useHealthQuery } from '../api/queries';

function Home() {
  const { data, isLoading, error } = useHealthQuery();

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">
        Welcome to Full-Stack App
      </h1>
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-semibold mb-2">Server Status</h2>
        {isLoading ? (
          <p className="text-gray-600">Loading...</p>
        ) : error ? (
          <p className="text-red-600">Error: {error.message}</p>
        ) : (
          <div>
            <p className="text-green-600">Status: {data?.status}</p>
            <p className="text-gray-600">Timestamp: {data?.timestamp}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Home;
