package org.batfish.representation.frr;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import javax.annotation.Nonnull;
import javax.annotation.ParametersAreNonnullByDefault;

/** Represents a Cumulus AS-path access list. */
@ParametersAreNonnullByDefault
public class BgpAsPathAccessList implements Serializable {

  private final @Nonnull String _name;
  private final @Nonnull List<BgpAsPathAccessListLine> _lines;

  public BgpAsPathAccessList(String name) {
    _name = name;
    _lines = new ArrayList<>();
  }

  public void addLine(BgpAsPathAccessListLine line) {
    _lines.add(line);
  }

  public @Nonnull List<BgpAsPathAccessListLine> getLines() {
    return _lines;
  }

  public @Nonnull String getName() {
    return _name;
  }
}
