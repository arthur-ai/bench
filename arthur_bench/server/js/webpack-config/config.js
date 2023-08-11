const webpack = require('webpack');
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: './index.tsx',
    target: 'web',
    mode: process.env.NODE_ENV || 'development',
    devServer: {
        historyApiFallback: true
    },
    resolve: {
        extensions: ['.js', '.ts', '.tsx'],
        alias: {
            react: path.resolve('./node_modules/react'),
            '@src': path.resolve(__dirname, '../src'),
            '@core': 'ui/core',
            '@compound': 'ui/compound',
        },
    },
    output: {
        path: path.resolve(__dirname, '../dist'),
        filename: 'bundle.js',
        publicPath: '/',
        assetModuleFilename: 'static/images/[name][ext]',
        clean: true,
    },
    module: {
        rules: [
            {
                test: /\.(ts|tsx)$/,
                loader: 'ts-loader',
            },
            {
                test: /\.(png|svg|jpg|jpeg|gif|woff|woff2|eot|ttf|otf)$/i,
                type: 'asset/resource',
            },
            {
                test: /\.(scss|css)$/,
                use: ['style-loader', 'css-loader'],
            },
        ],
    },
    plugins: [
        new HtmlWebpackPlugin({
            hash: true,
            title: process.env.APP_NAME || 'Untitled',
            template: './src/index.html',
            favicon: './public/arthur-triangle-favicon.png',
        }),
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: JSON.stringify(process.env.NODE_ENV),
                WITH_MOCKS: JSON.stringify(process.env.WITH_MOCKS),
                WITH_REMOTE: JSON.stringify(process.env.WITH_REMOTE),
            },
            'global': {},
        }),
        new webpack.IgnorePlugin({
            resourceRegExp: /^\.\/locale$/,
            contextRegExp: /moment$/,
        }),
    ],
    devtool: 'nosources-source-map',
    performance: {
        hints: false,
    },
    stats: {
        errorDetails: true,
        children: true
     },
};
