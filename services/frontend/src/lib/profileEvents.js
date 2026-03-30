export const PROFILE_LIST_CHANGED_EVENT = "chronicle:profile-list-changed";

export function notifyProfileListChanged() {
  window.dispatchEvent(new Event(PROFILE_LIST_CHANGED_EVENT));
}
