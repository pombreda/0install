(* Copyright (C) 2013, Thomas Leonard
 * See the README file for details, or visit http://0install.net.
 *)

(** Provides feeds to the solver. *)

class type feed_provider =
  object
    method forget_distro : Feed_url.non_distro_feed -> unit
    method forget_user_feeds : General.iface_uri -> unit
    method get_distro_impls : Feed.feed -> Impl.distro_implementation Support.Common.StringMap.t * Feed.feed_overrides
    method get_feed : Feed_url.non_distro_feed -> (Feed.feed * Feed.feed_overrides) option
    method get_feeds_used : Feed_url.non_distro_feed list
    method get_iface_config : General.iface_uri -> Feed_cache.interface_config
    method have_stale_feeds : bool
    method replace_feed : Feed_url.non_distro_feed -> Feed.feed -> unit
    method was_used : Feed_url.non_distro_feed -> bool
  end
