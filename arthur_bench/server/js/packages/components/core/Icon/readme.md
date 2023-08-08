# Icon Component

Usage

1. Import Icon component whenever you need it to render
2. Pass the right icon `type`, the complete list of available icon types can be found in file `types.ts`

How to add new icon type

1. go to https://icomoon.io/
2. register account if you don't have one and authorize
3. got to set redactor page https://icomoon.io/app/#/select
4. drop there your new icons svg
5. upload existing `selection.json` file from `packages/resources/icons/` folder
6. reset colors for new icons
7. click generate font
8. upload `selection.json` from the generated archive to the `packages/resources/icons` folder
9. add new icon types to the existing `Icon` type definitions `packages/ui/Icon/types.ts`
