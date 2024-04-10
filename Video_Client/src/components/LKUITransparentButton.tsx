import React from 'react';

interface LKUITransparentButtonProps {
  regComponent: React.ComponentType;
  ref?: React.RefObject<HTMLDivElement>;
  className?: string;
  title?: string;
  onClick?: (() => void) | undefined;
}

function LKUITransparentButton({ regComponent, ref, onClick, className, title }: LKUITransparentButtonProps) {
  const Icon = regComponent;

  return (
    <div className={`lkui-transparent-button ${className || ''}`} ref={ref} title={title} onClick={onClick}>
      <Icon />
    </div>
  );
}

export default LKUITransparentButton;
