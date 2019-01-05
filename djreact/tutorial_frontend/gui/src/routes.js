import React from 'react';
import { Route } from 'react-router-dom';

import ArticleList from './containers/ArticleListView';
import ArticleDetail from './containers/ArticleDetailView';
import Board from './containers/Tile';

const BaseRouter = () => (
    <div>
        <Route exact path='/' component={ArticleList}/>
        <Route exact path='/:articleID' component={ArticleDetail}/>
        <Route exact path='/test/game' component={Board}/>
    </div>
);

export default BaseRouter;