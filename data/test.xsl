<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
  <xsl:output method="text"/>

  <xsl:template match="/">
    <xsl:apply-templates select="/network/resolver/mappings"/>
  </xsl:template>

  <xsl:template match="/network/resolver/mappings">
    <xsl:text># Do not remove the following line, or various programs&#10;</xsl:text>
    <xsl:text># that require network functionality will fail.&#10;</xsl:text>
    <xsl:for-each select="map">
      <xsl:value-of select="@address"/>
      <xsl:text>&#09;&#09;</xsl:text>
      <xsl:value-of select="@hostname"/>
      <xsl:text>&#09;</xsl:text>
      <xsl:value-of select="@alias"/>
      <xsl:text>&#09;</xsl:text>
      <xsl:text>&#10;</xsl:text>
    </xsl:for-each>
  </xsl:template>

</xsl:stylesheet>
