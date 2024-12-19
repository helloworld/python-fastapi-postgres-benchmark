package org.batfish.specifier.parboiled;

import static com.google.common.base.MoreObjects.firstNonNull;
import static com.google.common.base.Preconditions.checkArgument;

import com.google.common.annotations.VisibleForTesting;
import com.google.common.base.MoreObjects;
import java.util.NoSuchElementException;
import java.util.Objects;
import java.util.Set;
import javax.annotation.Nonnull;
import org.batfish.datamodel.AclIpSpace;
import org.batfish.datamodel.EmptyIpSpace;
import org.batfish.datamodel.IpRange;
import org.batfish.datamodel.IpSpace;
import org.batfish.specifier.Grammar;
import org.batfish.specifier.IpSpaceAssignment;
import org.batfish.specifier.IpSpaceAssignmentSpecifier;
import org.batfish.specifier.IpSpaceSpecifier;
import org.batfish.specifier.Location;
import org.batfish.specifier.LocationIpSpaceSpecifier;
import org.batfish.specifier.ReferenceAddressGroupIpSpaceSpecifier;
import org.batfish.specifier.SpecifierContext;
import org.parboiled.errors.InvalidInputError;
import org.parboiled.parserunners.ReportingParseRunner;
import org.parboiled.support.ParsingResult;

/**
 * An {@link IpSpaceAssignmentSpecifier} and {@link IpSpaceSpecifier} that resolves based on the AST
 * generated by {@link org.batfish.specifier.parboiled.Parser}.
 */
public final class ParboiledIpSpaceSpecifier
    implements IpSpaceAssignmentSpecifier, IpSpaceSpecifier {

  static final class IpSpaceAstNodeToIpSpace implements IpSpaceAstNodeVisitor<IpSpace> {
    private final SpecifierContext _ctxt;

    IpSpaceAstNodeToIpSpace(SpecifierContext ctxt) {
      _ctxt = ctxt;
    }

    @Override
    public @Nonnull IpSpace visitDifferenceIpSpaceAstNode(
        DifferenceIpSpaceAstNode differenceIpSpaceAstNode) {
      // using firstNonNull to stop compiler warning. since neither left nor right should will be
      // null, the difference will not be null
      return firstNonNull(
          AclIpSpace.difference(
              differenceIpSpaceAstNode.getLeft().accept(this),
              differenceIpSpaceAstNode.getRight().accept(this)),
          EmptyIpSpace.INSTANCE);
    }

    @Override
    public @Nonnull IpSpace visitIntersectionIpSpaceAstNode(
        IntersectionIpSpaceAstNode intersectionIpSpaceAstNode) {
      // using firstNonNull to stop compiler warning. since neither left nor right should will be
      // null, the intersection will not be null
      return firstNonNull(
          AclIpSpace.intersection(
              intersectionIpSpaceAstNode.getLeft().accept(this),
              intersectionIpSpaceAstNode.getRight().accept(this)),
          EmptyIpSpace.INSTANCE);
    }

    @Override
    public @Nonnull IpSpace visitUnionIpSpaceAstNode(UnionIpSpaceAstNode unionIpSpaceAstNode) {
      // using firstNonNull to stop compiler warning. since neither left nor right should will be
      // null, the union will not be null
      return firstNonNull(
          AclIpSpace.union(
              unionIpSpaceAstNode.getLeft().accept(this),
              unionIpSpaceAstNode.getRight().accept(this)),
          EmptyIpSpace.INSTANCE);
    }

    @Override
    public @Nonnull IpSpace visitIpAstNode(IpAstNode ipAstNode) {
      return ipAstNode.getIp().toIpSpace();
    }

    @Override
    public @Nonnull IpSpace visitIpRangeAstNode(IpRangeAstNode rangeIpSpaceAstNode) {
      return IpRange.range(rangeIpSpaceAstNode.getLow(), rangeIpSpaceAstNode.getHigh());
    }

    @Override
    public @Nonnull IpSpace visitIpWildcardAstNode(IpWildcardAstNode ipWildcardAstNode) {
      return ipWildcardAstNode.getIpWildcard().toIpSpace();
    }

    @Override
    public @Nonnull IpSpace visitLocationIpSpaceAstNode(
        LocationIpSpaceAstNode locationIpSpaceAstNode) {
      return LocationIpSpaceSpecifier.computeIpSpace(
          new ParboiledLocationSpecifier(locationIpSpaceAstNode.getLocationAst()).resolve(_ctxt),
          _ctxt);
    }

    @Override
    public @Nonnull IpSpace visitPrefixAstNode(PrefixAstNode prefixAstNode) {
      return prefixAstNode.getPrefix().toIpSpace();
    }

    @Override
    public @Nonnull IpSpace visitAddressGroupAstNode(
        AddressGroupIpSpaceAstNode addressGroupIpSpaceAstNode) {
      // Because we changed the input on Apr 30 2019 from (group, book) to (book, group), we
      // first interpret the user input as (book, group) if the book exists. Otherwise, we interpret
      // it is as (group, book)
      if (_ctxt.getReferenceBook(addressGroupIpSpaceAstNode.getReferenceBook()).isPresent()) {
        return ReferenceAddressGroupIpSpaceSpecifier.computeIpSpace(
            addressGroupIpSpaceAstNode.getAddressGroup(),
            addressGroupIpSpaceAstNode.getReferenceBook(),
            _ctxt);
      } else if (_ctxt.getReferenceBook(addressGroupIpSpaceAstNode.getAddressGroup()).isPresent()) {
        return ReferenceAddressGroupIpSpaceSpecifier.computeIpSpace(
            addressGroupIpSpaceAstNode.getReferenceBook(),
            addressGroupIpSpaceAstNode.getAddressGroup(),
            _ctxt);
      }
      throw new NoSuchElementException(
          "Reference book " + addressGroupIpSpaceAstNode.getReferenceBook() + " does not exist.");
    }
  }

  private final IpSpaceAstNode _ast;

  ParboiledIpSpaceSpecifier(IpSpaceAstNode ast) {
    _ast = ast;
  }

  /**
   * Returns an {@link IpSpaceAssignmentSpecifier} based on {@code input} which is parsed as {@link
   * Grammar#IP_SPACE_SPECIFIER}.
   *
   * @throws IllegalArgumentException if the parsing fails or does not produce the expected AST
   */
  public static ParboiledIpSpaceSpecifier parse(String input) {
    ParsingResult<AstNode> result =
        new ReportingParseRunner<AstNode>(
                Parser.instance().getInputRule(Grammar.IP_SPACE_SPECIFIER))
            .run(input);

    if (!result.parseErrors.isEmpty()) {
      throw new IllegalArgumentException(
          ParserUtils.getErrorString(
              input,
              Grammar.IP_SPACE_SPECIFIER,
              (InvalidInputError) result.parseErrors.get(0),
              Parser.ANCHORS));
    }

    AstNode ast = ParserUtils.getAst(result);
    checkArgument(
        ast instanceof IpSpaceAstNode, "ParboiledIpSpaceSpecifier requires an IpSpace input");

    return new ParboiledIpSpaceSpecifier((IpSpaceAstNode) ast);
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (!(o instanceof ParboiledIpSpaceSpecifier)) {
      return false;
    }
    return Objects.equals(_ast, ((ParboiledIpSpaceSpecifier) o)._ast);
  }

  @Override
  public int hashCode() {
    return Objects.hashCode(_ast);
  }

  @Override
  public IpSpaceAssignment resolve(Set<Location> locations, SpecifierContext ctxt) {
    IpSpace ipSpace = computeIpSpace(_ast, ctxt);
    return IpSpaceAssignment.builder().assign(locations, ipSpace).build();
  }

  @Override
  public IpSpace resolve(SpecifierContext ctxt) {
    return computeIpSpace(_ast, ctxt);
  }

  @VisibleForTesting
  static @Nonnull IpSpace computeIpSpace(IpSpaceAstNode ast, SpecifierContext ctxt) {
    return ast.accept(new IpSpaceAstNodeToIpSpace(ctxt));
  }

  @Override
  public String toString() {
    return MoreObjects.toStringHelper(getClass()).add("ast", _ast).toString();
  }
}