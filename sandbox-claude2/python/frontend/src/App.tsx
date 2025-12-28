import { BrowserRouter, Routes, Route } from "react-router-dom"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import Home from "./pages/Home"
import NewEvent from "./pages/NewEvent"
import EventDetail from "./pages/EventDetail"

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/new" element={<NewEvent />} />
          <Route path="/event/:id" element={<EventDetail />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
