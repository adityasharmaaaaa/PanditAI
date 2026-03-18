import * as React from "react";

type IconProps = {
  size?: number;
  strokeWidth?: number;
  className?: string;
  title?: string;
};

function IconBase({
  size = 20,
  strokeWidth = 1.6,
  className,
  title,
  children,
}: IconProps & { children: React.ReactNode }) {
  const ariaHidden = title ? undefined : true;
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden={ariaHidden}
      role={title ? "img" : "presentation"}
    >
      {title ? <title>{title}</title> : null}
      {children}
    </svg>
  );
}

export function IconDashboard(props: IconProps) {
  return (
    <IconBase {...props}>
      <rect x="3" y="3" width="8" height="8" rx="2" />
      <rect x="13" y="3" width="8" height="5" rx="2" />
      <rect x="13" y="10" width="8" height="11" rx="2" />
      <rect x="3" y="13" width="8" height="8" rx="2" />
    </IconBase>
  );
}

export function IconCompass(props: IconProps) {
  return (
    <IconBase {...props}>
      <circle cx="12" cy="12" r="9" />
      <path d="M14.5 9.5l-2.5 5-2.5 2.5 2.5-5 2.5-2.5z" />
    </IconBase>
  );
}

export function IconHourglass(props: IconProps) {
  return (
    <IconBase {...props}>
      <path d="M6 3h12" />
      <path d="M6 21h12" />
      <path d="M8 3c0 4 8 4 8 8s-8 4-8 8" />
    </IconBase>
  );
}

export function IconCrown(props: IconProps) {
  return (
    <IconBase {...props}>
      <path d="M4 7l4 4 4-6 4 6 4-4v8H4z" />
      <path d="M4 19h16" />
    </IconBase>
  );
}

export function IconMessage(props: IconProps) {
  return (
    <IconBase {...props}>
      <path d="M4 5h16a3 3 0 0 1 3 3v7a3 3 0 0 1-3 3H9l-5 4v-4H4a3 3 0 0 1-3-3V8a3 3 0 0 1 3-3z" />
    </IconBase>
  );
}

export function IconWallet(props: IconProps) {
  return (
    <IconBase {...props}>
      <rect x="3" y="6" width="18" height="12" rx="2" />
      <path d="M16 10h4v4h-4z" />
      <path d="M3 8h14" />
    </IconBase>
  );
}

export function IconBriefcase(props: IconProps) {
  return (
    <IconBase {...props}>
      <rect x="3" y="7" width="18" height="12" rx="2" />
      <path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2" />
      <path d="M3 13h18" />
    </IconBase>
  );
}

export function IconHeart(props: IconProps) {
  return (
    <IconBase {...props}>
      <path d="M20 8.5c0 4.2-8 9.5-8 9.5s-8-5.3-8-9.5A4.5 4.5 0 0 1 12 6a4.5 4.5 0 0 1 8 2.5z" />
    </IconBase>
  );
}

export function IconSparkles(props: IconProps) {
  return (
    <IconBase {...props}>
      <path d="M12 3l1.6 3.6L17 8l-3.4 1.4L12 13l-1.6-3.6L7 8l3.4-1.4L12 3z" />
      <path d="M5 14l1 2 2 1-2 1-1 2-1-2-2-1 2-1 1-2z" />
    </IconBase>
  );
}

export function IconSend(props: IconProps) {
  return (
    <IconBase {...props}>
      <path d="M3 11.5l18-8-6.5 18-2.8-6.2L3 11.5z" />
      <path d="M12.7 15.3L21 3.5" />
    </IconBase>
  );
}

export function IconUser(props: IconProps) {
  return (
    <IconBase {...props}>
      <circle cx="12" cy="8" r="4" />
      <path d="M4 21a8 8 0 0 1 16 0" />
    </IconBase>
  );
}

export function IconStar(props: IconProps) {
  return (
    <IconBase {...props}>
      <path d="M12 3l2.6 5.4 6 0.9-4.3 4.2 1 6-5.3-2.8-5.3 2.8 1-6L3.4 9.3l6-0.9L12 3z" />
    </IconBase>
  );
}

export function IconArrowLeft(props: IconProps) {
  return (
    <IconBase {...props}>
      <path d="M15 6l-6 6 6 6" />
      <path d="M9 12h12" />
    </IconBase>
  );
}

export function IconCheck(props: IconProps) {
  return (
    <IconBase {...props}>
      <path d="M5 12l4 4 10-10" />
    </IconBase>
  );
}

export function IconChevronDown(props: IconProps) {
  return (
    <IconBase {...props}>
      <path d="M6 9l6 6 6-6" />
    </IconBase>
  );
}

export function IconChevronUp(props: IconProps) {
  return (
    <IconBase {...props}>
      <path d="M6 15l6-6 6 6" />
    </IconBase>
  );
}
