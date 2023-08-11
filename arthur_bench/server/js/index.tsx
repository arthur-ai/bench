import React from 'react';
import { createRoot } from 'react-dom/client'
import { Provider as StateProvider } from 'react-redux';
import { store } from 'arthur-redux';
import 'resources/icons/selection';
import 'resources/fonts/fonts.css';
import Skin from './src/Skin/skin';


const element = document.getElementById('root') as HTMLElement;
const root = createRoot(element);

root.render(
    <StateProvider store={store}>
        <Skin />
    </StateProvider>
);
