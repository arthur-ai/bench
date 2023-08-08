import primary from 'resources/colors/Arthur/primary';
import { dropdownStyles } from '../MultipleSelect/styles';

export const searchStyles = {
    width: '200px',
    height: '32px',
    boxSizing: 'border-box',
};

export const searchContainer = {
    paddingLeft: '10px',
};

export const defaultStyle = {
    backgroundColor: primary.white,
    position: 'relative',
    boxSizing: 'border-box',
    minHeight: '32px',
    borderRadius: '2px 2px 0px 0px',
    boxShadow: '0px 1px 5px rgba(0, 0, 0, 0.1)',
};

export const paginationContainer = {
    display: 'flex',
    flexDirection: 'column',
    padding: '5px 0 10px',
    justifyContent: 'end',
};

export const selectedAreaStyle = {
    display: 'flex',
    overflow: 'scroll',
    maxHeight: '150px',
};

export const selectedTagColumn = {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '6px',
    padding: '10px',
};

export const selectedTagStyle = {
    display: 'flex',
    boxSizing: 'border-box',
    justifyContent: 'space-between',
};

export const optionStyle = {
    boxSizing: 'border-box',
    height: '32px',
    padding: '2px 12px',
    border: '1px solid lightgray',
    borderRadius: 0,
    color: 'red',
};

export const renderSelectAllContainer = {
    padding: '4px 0px',
};

export const optionStyleContainer = {
    padding: '4px 0px',
};

export const optionsStyles = {
    padding: '0 10px',
    width: '100%',
    maxHeight: '330px',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'scroll',
    boxSizing: 'border-box',
};

export const optionStylesContainer = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'end',
};

export const optionsDropdownFooter = {
    height: '64px',
    display: 'flex',
    gap: '10px',
    boxShadow: 'inset 0px 1px 0px rgba(26, 0, 22, 0.1)',
    borderRadius: '0px 0px 2px 2px',
    justifyContent: 'end',
    alignItems: 'center',
    paddingRight: '20px',
};

export const dropdownRootStyles = {
    ...dropdownStyles,
    borderRadius: '0 0 2px 2px',
    width: '312px',
};
