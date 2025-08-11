import LandingPage from './components/landingPage/landing';
import { UserContext } from 'context/userContext';
import { ProcessContext } from 'context/processContext';
import './App.css';
import { useMemo, useState } from 'react';
import LoadingPage from 'components/loadingPage/loadingPage';
import ResultPage from 'components/resultPage/resultPage';
import { SummaryContext } from 'context/summaryContext';
import {
  createBrowserRouter,
  RouterProvider,
  Route
} from "react-router-dom";
import { SearchParamContext } from 'context/modalContext';

const router = createBrowserRouter([
  {
    path: "/",
    element: <LandingPage/>,
  },
  {
    path: "/loading",
    element: <LoadingPage/>,
  },
  {
    path: "/results",
    element: <ResultPage/>,
  },
]);

function App() {

  const [userContext, setUserContext] = useState(null);
  const providerUserContext = useMemo(() => ({userContext, setUserContext}), [userContext, setUserContext]);

  const [processContext, setProcessContext] = useState(null);
  const providerProcessContext = useMemo(() => ({processContext, setProcessContext}), [processContext, setProcessContext]);

  const [summaryContext, setSummaryContext] = useState(null);
  const providerSummaryContext = useMemo(() => ({summaryContext, setSummaryContext}), [summaryContext, setSummaryContext]);

  return (
    <div className="App">
      <ProcessContext.Provider value = {providerProcessContext}>
        <UserContext.Provider value = {providerUserContext}>
          <SummaryContext.Provider value = {providerSummaryContext}>
            <RouterProvider router={router} />
          </SummaryContext.Provider>
        </UserContext.Provider>
      </ProcessContext.Provider>
    </div>
  );
}

export default App;
